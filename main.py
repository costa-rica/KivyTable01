from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
import json
import datetime

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class TableScreen(Screen):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    print('TableScreen __init__')

  def on_kv_post(self,*args):
    #get count of row_data_list
    print('Need table grid:::', self.children[0].children[0].children[0].children[1].children[0])
    self.table_grid = self.children[0].children[0].children[0].children[1].children[0]
    count=len(self.table_grid.row_data_list)
    #populate record_count_label with count
    self.record_count_label.text="User Entries Count: " +str(count)



class TableGrid(GridLayout):
  row_count=StringProperty()
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    print('TableGrid __init__')
    self.cols=1
    self.spacing=5
    self.size_hint=(1,None)
    self.row_data_list=MainApp.get_running_app().row_data_list
    self.table_size='20'
    self.row_count_showing="0"
    self.build_table()
    self.button_dict={'ID':0,'Date/Time':0,'Activity Name':0,'All/Last 20':0,'Showing':0}
    self.on_size_count=0
    # self.on_children_count=0
    self.sort_util_flag=False#reduce the numbrer of times rowbox_font_size_util get's called
    self.bind(size=self.rowbox_font_size_util)



  def on_kv_post(self,*args):
    print('TableGrid on_kv_post')
    self.table_screen= self.parent.parent.parent.parent.parent
    self.table_screen.fancy_header.delete_column.text =f"Showing {self.table_size} entries"
    # self.rowbox_dict[0].act_id.font_size=self.table_screen.width*.12
    # self.sort_util_flag=True
    # self.rowbox_font_size_util()
    # self.sort_util_flag=False


  def delete_act(self,widget):
    #CAll to api for delete
    self.row_data_list=[x for x in self.row_data_list if widget.name not in x]
    self.row_count_showing=str(len(self.row_data_list))
    self.table_screen.record_count_label.text="Row Count: " +self.row_count_showing
    self.clear_widgets()
    self.build_table()

  def build_table(self):
    print('TableGrid build_table')
    row_data_list = self.row_data_list[0:20] if self.table_size=='20' else self.row_data_list
    self.row_count_showing=str(len(row_data_list))
    self.rowbox_dict={}
    for h,i in enumerate(row_data_list):

      rowbox = RowBox(size_hint=(1,None))
      rowbox.act_id.text=i[0]
      rowbox.act_id.color=(.5,.1,.1,1)
      rowbox.act_date.text=i[1]
      rowbox.act_name.text=i[2]
      rowbox.act_delete.text="delete"
      rowbox.act_delete.name = i[0]
      self.add_widget(rowbox)
      self.rowbox_dict[h]=rowbox


  def sort_util(self,widget):
    if widget.text[:2]=="ID":

      self.button_dict['ID']+=1
      if self.button_dict['ID']%3==0:#no sort
        self.table_screen.fancy_header.id_btn.text="ID"
        self.table_screen.fancy_header.id_btn.background_color=(1,1,1,1)
        self.row_data_list.sort(key=lambda k: k[4])

      elif self.button_dict['ID']%3==1:#ascending
        self.table_screen.fancy_header.id_btn.text="ID \n ascending"
        self.table_screen.fancy_header.id_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k: k[0])


      elif self.button_dict['ID']%3==2:#descending
        self.table_screen.fancy_header.id_btn.text="ID \n descending"
        self.table_screen.fancy_header.id_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k: k[0],reverse=True)

      self.table_screen.fancy_header.date_btn.text="Date/Time"
      self.table_screen.fancy_header.date_btn.background_color=(1,1,1,1)
      self.table_screen.fancy_header.act_btn.text="Activity Name"
      self.table_screen.fancy_header.act_btn.background_color=(1,1,1,1)

    if widget.text[:2]=='Da':
      self.button_dict['Date/Time']+=1
      if self.button_dict['Date/Time']%3==0:#no sort
        self.table_screen.fancy_header.date_btn.text="Date/Time"
        self.table_screen.fancy_header.date_btn.background_color=(1,1,1,1)
        self.row_data_list.sort(key=lambda k:k[4])
      elif self.button_dict['Date/Time']%3==1:#ascending
        self.table_screen.fancy_header.date_btn.text="Data/Time \n ascending"
        self.table_screen.fancy_header.date_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k:k[3])
      elif self.button_dict['Date/Time']%3==2:#descending
        self.table_screen.fancy_header.date_btn.text="Data/Time \n descending"
        self.table_screen.fancy_header.date_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k:k[3],reverse=True)

      self.table_screen.fancy_header.id_btn.text="ID"
      self.table_screen.fancy_header.id_btn.background_color=(1,1,1,1)
      self.table_screen.fancy_header.act_btn.text="Activity Name"
      self.table_screen.fancy_header.act_btn.background_color=(1,1,1,1)

    if widget.text[:2]=='Ac':
      # print('Activity Name button pressed')
      self.button_dict['Activity Name']+=1
      if self.button_dict['Activity Name']%3==0:#no sort
        self.table_screen.fancy_header.act_btn.text="Activity Name"
        self.table_screen.fancy_header.act_btn.background_color=(1,1,1,1)
        self.row_data_list.sort(key=lambda k:k[4])
      elif self.button_dict['Activity Name']%3==1:#ascending
        self.table_screen.fancy_header.act_btn.text="Activity Name \n ascending"
        self.table_screen.fancy_header.act_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k:k[2])
      elif self.button_dict['Activity Name']%3==2:#descending
        self.table_screen.fancy_header.act_btn.text="Activity Name \n descending"
        self.table_screen.fancy_header.act_btn.background_color=(.3,.3,.3,1)
        self.row_data_list.sort(key=lambda k:k[2],reverse=True)

      self.table_screen.fancy_header.id_btn.text="ID"
      self.table_screen.fancy_header.id_btn.background_color=(1,1,1,1)
      self.table_screen.fancy_header.date_btn.text="Date/Time"
      self.table_screen.fancy_header.date_btn.background_color=(1,1,1,1)

    if widget.text[:2]=='Sh':
      self.button_dict['Showing']+=1
      if self.button_dict['Showing']%2==0:
        self.table_size='20'
        self.build_table()
        self.table_screen.fancy_header.delete_column.text =f"Showing {self.row_count_showing} entries"
        # self.table_screen.record_count_label.text="Row Count: " +str(len(self.row_data_list))
      elif self.button_dict['Showing']%2==1:
        self.table_size='All'
        self.build_table()
        self.table_screen.fancy_header.delete_column.text =f"Showing {self.row_count_showing} \n (All) entries"
        # self.table_screen.record_count_label.text="Row Count: " +str(len(self.row_data_list)) +'\n (All)'

    self.clear_widgets()
    self.build_table()
    self.sort_util_flag=True
    self.rowbox_font_size_util()
    self.sort_util_flag=False


  def rowbox_font_size_util(self,*args):
    print('TableGrid in rowbox_font_size_util: ', self.on_size_count)
    if self.on_size_count==4 or self.sort_util_flag:
      table_font_size=self.table_screen.width*.015
      for i,j in self.rowbox_dict.items():
        j.act_id.font_size=table_font_size
        j.act_date.font_size=table_font_size
        j.act_name.font_size=table_font_size
        j.act_delete.font_size=table_font_size
    self.on_size_count+=1
    # self.on_children_count+=1



class RowBox(BoxLayout):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)


class MainApp(MDApp):
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    print('MainApp __init__')
    self.base_url = 'https://api.what-sticks-health.com'

  def build(self):
    self.login()
    self.row_data_list=self.table_data_util()
    return Builder.load_file('tablescreen.kv')

  def login(self):
    self.base_url = 'https://api.what-sticks-health.com'
    response_login = requests.request('GET',self.base_url + '/login',
        auth=('guest@what-sticks-health.com','test'))
    self.login_token = json.loads(response_login.content.decode('utf-8'))['token']

  def table_data_util(self):
    url_get_activities=self.base_url + '/kivy_table01'
    headers = {'x-access-token':self.login_token, 'Content-Type': 'application/json'}
    response = requests.request('GET',url_get_activities, headers=headers)
    response_dict = json.loads(response.text)

    row_data_list=[
    [i[0],self.convert_datetime(i[1]),i[2], self.make_date_string(i[1]), h] for h,i in enumerate(response_dict['content'])
    ]
    return row_data_list

  def convert_datetime(self, date_time_str):
      try:
          date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
      except ValueError:
          # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
          print("""There is an error converting datetimes in
          scroll_table_data.py or with API call to kivy_table01""")
      # return date_time_obj.strftime("%m/%d/%Y, %H:%M:%S")
      return date_time_obj.strftime("%b%-d '%-y %-I:%M%p")#<------Potential hangup!***************!

  def make_date_string(self, date_time_str):
      date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
      return date_time_obj.strftime('%Y%m%d')


if __name__=='__main__':
  MainApp().run()
