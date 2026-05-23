import mysql.connector
import pandas as pd

class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'zain',
                database = 'sql_join_lecture'
            )
            self.mycursor = self.conn.cursor()
            print("Connection Established Successfully!!")
        except Exception as e:
            print(e)
            
    
    def fetch_city_name(self):
        city = []
        self.mycursor.execute("""
            SELECT DISTINCT(Destination) FROM flights
            UNION
            SELECT DISTINCT(Source) FROM flights
                              """)
        
        for i in self.mycursor.fetchall():
            city.append(i[0])
            
        return city
    
    def fetch_all_flights(self, source, destination):
        
        query = f"""
            SELECT Airline,Date_of_Journey,Route,Dep_Time,Duration,Price
            FROM flights
            WHERE SOURCE = '{source}' AND Destination = '{destination}'
        """
        
        self.mycursor.execute(query)
        
        data = (self.mycursor.fetchall())
        
        df = pd.DataFrame(
            data,
            columns=['Airline','Date_of_Journey','Route','Dep_Time','Duration','Price']
        )

        return df
    
    def fetch_airline_count(self):
        query = """
        SELECT Airline, Count(*) FROM flights
        GROUP BY Airline
        ORDER BY Count(*) DESC
        """
        
        self.mycursor.execute(query)
        
        data = (self.mycursor.fetchall())
        
        df = pd.DataFrame(
            data,
            columns=['Airline','Count']
        )

        return df
    
    def fetch_all(self):
        query = """
        SELECT * FROM flights
        """
        
        self.mycursor.execute(query)
        
        data = (self.mycursor.fetchall())
        
        df = pd.DataFrame(
            data,
            columns=['Airline', 'Date_of_Journey', 'Source', 'Destination', 'Route', 'Dep_Time', 'Duration', 'Total_Stops', 'Price']
        )

        return df
    
    def busy_airport(self):
        
        query = """
        SELECT city, Count(*) FROM (
            SELECT Source AS city FROM flights
            UNION ALL
            SELECT Destination FROM flights
        ) t
        GROUP BY city
        ORDER BY Count(*) DESC
        """
        
        self.mycursor.execute(query)
        
        data = (self.mycursor.fetchall())
        
        df = pd.DataFrame(
            data,
            columns=['City','Count']
        )

        return df