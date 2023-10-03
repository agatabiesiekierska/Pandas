
# Source: https://www.dataquest.io/blog/python-tutorial-analyze-personal-netflix-data/

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

class Empty_Data_Frame(Exception):
    def __init__(self,text):
        super().__init__(text)
    
    def __str__(self):
        return f'{super.__str__(self)}'

class Dokument:

# initializing the object
    def __init__(self,path):
        self.path = path
        self.df = self.__load_data()

# imports the data from .csv into dataframe (df)
    def __load_data(self):
        df = pd.read_csv(self.path,delimiter =',')
        return df 

# displays the dataframe
    def read_data(self):
        print(self.df)
        return self.df

# shows basic info about the dataframe
    def show_info(self):
        print('The number of rows and columns in the dataframe: ', self.df.shape)
        print('The first five rows of the dataframe:\n', self.df.head())


# This function works with time data   
    def Convert_to_time(self):
        # Converting strings with data into date_time with utc timezone attached to it (utc = true)
        self.df['Start Time'] = pd.to_datetime(self.df['Start Time'], utc=True) 

        # Changing the Start Time column into dataframe's index (we have to do this to use .tz_convert())
        self.df =  self.df.set_index('Start Time')

        # Conversion from UTC timezone to Central European Time (CET)
        self.df.index =  self.df.index.tz_convert('CET')
        
        # reset the index so that Start Time becomes a column again
        self.df = self.df.reset_index()

        # Convertsion duration time into timedelta
        self.df['Duration'] = pd.to_timedelta(self.df['Duration'])

        return self.df

''' a new class for file with data about Gaming activity on Netflix account
class GamePlaySession(Dokument):
    'This Class is being dedicated to document GameActivity.csv'
    def __init__(self, path):
        super().__init__(path)
    
    def show_info(self):
        super().show_info()


# Drop unnecessary columns from dataframe
    def drop_unneces_col(self):
        self.df = self.df.drop(['Game Version', 'Platform', 'Device Type', 'Country', 'Esn', 'Ip'], axis=1)
        return self.df
'''

class ViewingActivity(Dokument):
    'This class is being dedicated to document ViewingActivity.csv'
    
    def __init__(self, path):
        super().__init__(path)
        self.series = pd.DataFrame()
    
    def show_info(self):
        super().show_info()
        print(35*'=')
        print(f'The phrase you are looking for: {self.title}')
        print(f'The user you are looking for: {self.name}')
        print(f'How much time do you spend watching this series?: {self.how_much_time}')



    def drop_unneces_col(self):
        # This function deletes columns from datadrame we're not planning to use
        
        self.df = self.df.drop(['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
        return self.df
    
    def search_for_the_series(self,title,name = ''):
        # Creates a new dataframe that takes from dataframe only the rows in which the Title column contains the given title and Profile name column contains the given name. 
        # regex = False tells the function that the name argument is a string and not a regular expression.
        # If the series isn't in DataFrame, programm will stop and the user will get a notification
        try:
            self.title = title
            self.name = name
            self.series = self.df[self.df['Profile Name'].str.contains(name, regex=False)]
            self.series = self.df[self.df['Title'].str.contains(title, regex=False)]
            if self.series.empty:
                raise Empty_Data_Frame('There is no such series in this DataFrame or the name was entered incorrectly. Delete white signs and remember about Big letters')
        except Empty_Data_Frame as e: print(f'There is a problem with your input!\nDetails: {e}')
        except Exception as e: print(f'An error has occured! \nDetails: {e}')
        return self.series
    
    def delete_short_duration(self):
        # This function removes from series dataframe records, where duration time is shorter than 1 minute

        self.series = self.series[(self.series['Duration'] > '0 days 00:01:00')]
        return self.series
    
    def analysis_series(self):
        # Sums all records from Duration column - the result is the total time of watching 
        self.how_much_time = self.series['Duration'].sum()

        # Search in Start Time column on which day of week and hour the user was watching this series.
        # Function assigns the results into new columns 'weekday' and 'hour'
        self.series['weekday'] = self.series['Start Time'].dt.weekday
        self.series['hour'] = self.series['Start Time'].dt.hour

    def plot_by_day(self):
        # This method will display data from analysis on plots.
        data_to_plot = self.series.copy()
        # setting the collumn from which we retrieve data and defining the order (mon - sun)
        data_to_plot['weekday'] = pd.Categorical(data_to_plot['weekday'], categories=[0,1,2,3,4,5,6],ordered=True)

        # creates variable by_day and counts the rows for each weekday then assigning the result 
        by_day = data_to_plot['weekday'].value_counts()

        # sorting the index (MON - 0; TUE - 1 etc.)
        by_day = by_day.sort_index()

        # changing the font size
        matplotlib.rcParams.update({'font.size': 22})

        # plot by_day as a bar chart with the listed size and title
        by_day.plot(kind='bar', figsize=(20,10), title=f'{self.title} Episodes Watched by Day by {self.name}')
        plt.show()

    def plot_by_hour(self):
        data_to_plot = self.series.copy()
        # setting categorical and defining the order
        data_to_plot['hour'] = pd.Categorical(data_to_plot['hour'], categories= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],ordered=True)

        # counts the rows for each hour and assigns the result
        by_hour = data_to_plot['hour'].value_counts()

        # sorting the index 
        by_hour = by_hour.sort_index()

        # plot by_hour as a bar chart with the listed size and title
        by_hour.plot(kind='bar', figsize=(20,10), title=f'{self.title} Episodes Watched by Hours by {self.name}')
        plt.show()

# Work in progress
# doc_1 = GamePlaySession(r'C:\Python - skrypty\Własne Projekty\Analiza Danych - Netflix\netflix-report\GAMES\GamePlaySession.csv')


# Initiating an object ViewingActivity, which refers to file ViewingActivity.csv (it contains the viewing data)
doc_2 = ViewingActivity(r'C:\Python - skrypty\Własne Projekty\Analiza Danych - Netflix\netflix-report\CONTENT_INTERACTION\ViewingActivity.csv')
doc_2.drop_unneces_col()
doc_2.Convert_to_time()
doc_2.search_for_the_series('Biuro:', 'Agata')
doc_2.analysis_series()
doc_2.show_info()
doc_2.plot_by_day()
doc_2.plot_by_hour()
