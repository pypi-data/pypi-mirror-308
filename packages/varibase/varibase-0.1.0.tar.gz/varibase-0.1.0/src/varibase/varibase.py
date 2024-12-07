import pickle
import threading
import warnings
import duckdb
import os
import time

class VarDB():

    def __init__(self):
        self.filename = None

        if self.filename is None:
            self.filename =  VarDB.get_filename().split('\\')[-1].split('.')[0]

        
        self.dd_name = f"{self.filename}.db"
        self.connection = duckdb.connect(self.dd_name)
        self.connection.execute("""create table if not exists variable_base (key varchar primary key,
                                                                            pickled_object blob,
                                                                            dtype varchar,
                                                                            timestamp timestamp default current_timestamp)""")
        self.last_runtime = time.time()
        self.lock = threading.Lock()
        self.stop_db_time = 2*3600

    def check_conn_alive(self):
        try:
            self.connection.execute("select 1").fetchone()

        except duckdb.ConnectionException:
            self.connection = duckdb.connect(self.dd_name)

    def store_var(self,key:str,variable):
        """
        Stores any variable into the variable DB. If key already exists in the db it will overwrite with the new variable with the same old key

        Parameters:
        -------------------
        key : str
            The key to store the variable under.
        variable : any
            The variable to be stored. Can be of any type.

        Returns:
        -------------------
        None

        Raises:
        -------------------
        TypeError
        If the `variable` contains objects that cannot be pickled, such as:
        - Open file handles and databse connections
        - Lambda functions
        - Generators or iterators
        - Custom objects without proper pickling support
        PicklingError
            If the pickling process fails due to unpickleable objects or unsupported data types.

        """
        pickled_object = pickle.dumps(variable)
        datatype = str(type(variable))
        self.check_conn_alive()
        with self.lock:
           self.last_runtime = time.time()
           with self.connection:
                
                self.connection.execute("""insert into variable_base (key,pickled_object,dtype) values (?,?,?)
                                        on conflict (key) do update set pickled_object = excluded.pickled_object , dtype=excluded.dtype""",(key,pickled_object,datatype))
                
    def fetch_var(self,key:str):
        """
        Fetches the variable previously stored in the db.

        Parameters:
        -------------------
        key : str
            The key to fetch the variable from.

        Returns:
        -------------------
        variable : any
            The variable fetched from the DB. Can be of any type. If the key is not found, returns None.

        """
        try:
            self.check_conn_alive()
            with self.lock:
                self.last_runtime = time.time()
                with self.connection:
                    result = self.connection.execute("""select pickled_object from variable_base where key = ?""",(key,)).fetchone()
                    
                    if result:
                        # print(result)
                        pickled_object = result[0]
                        return pickle.loads(pickled_object)
                    else:
                        warnings.warn(f"Variable {key} not found", UserWarning)
                        return None
                    
        except Exception as e:
            raise TypeError(f"There was an error:{e}")
            

    def check_time(self):
        while True:
            time.sleep(1)
            with self.lock:
                if time.time() -self.last_runtime >= self.stop_db_time:
                    self.close_connection()
                    break

    def close_connection(self):
        self.connection.close()


    def flush_db(self):
        """
        Closes the connection to the db and deletes all the stored variables
        """
        try:
            self.close_connection()
            os.remove(VarDB.get_filename().strip('.ipynb')+'.db')

        except Exception as e:
            raise TypeError(f"There was an error {e}")

    @staticmethod
    def get_filename():
        try:
            ip = get_ipython()
            paths = None
            if '__vsc_ipynb_file__' in ip.user_ns:
                paths =ip.user_ns['__vsc_ipynb_file__']
                return paths
            else:
                return "notebookname"
            
        except Exception as e:
            return "notebookname"
        