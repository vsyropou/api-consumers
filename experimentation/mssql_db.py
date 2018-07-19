import abc
import pymssql
import platform
import os
import json


__all__ = ['BaseMSsqlDatabaseConnector']

tmp_directory_path = ''

class AbsMSsqlDatabaseConnector(abc.ABC):

    @property
    @abc.abstractmethod
    def host(self):
        pass
    
    @property
    @abc.abstractmethod
    def user(self):
        pass

    @property
    @abc.abstractmethod
    def database(self):
        pass


class BaseMSsqlDatabaseConnector(AbsMSsqlDatabaseConnector):

    formaters = { 'base' : dict }

    
    def __init__(self):

        # check if tmp dir is set
        if not tmp_directory_path: 
            self._set_tmp_dir()        

        # check tmp dir path exists
        assert os.path.exists(tmp_directory_path), \
            'Path "%s" does not exist. Try specifieng path correctly or set the '\
            'global property "tmp_directory_path" accordingly'

        # look for password
        self._check_password()

        # connect to database
        self.connect()


    def _set_tmp_dir(self):
        
        global tmp_directory_path

        on_linux_machine = 'linux' in platform.platform().lower()
        if on_linux_machine: # on linux
            tmp_directory_path = '/tmp'
        else: # on windows
            ## TODO: Get tmp dir from environment
            msg1 = 'Windows os detected. Specify temporary directory path for caching:\n> '
            tmp_directory_path = input(msg1)
            print()

        return tmp_directory_path


    def _check_password(self):

        global tmp_directory_path
                
        classname = self.__class__.__name__
        prefix = classname.split('MSsqlDatabaseConnector')[0]

        self._credentials_path = os.path.join(tmp_directory_path,'%s_sql_crd.json'%prefix)
        if not os.path.exists(self._credentials_path):
            msg = 'Provide password for database "%s" (hostname: %s): \n> '%(prefix,self.host)
            pwd = input(msg)
            print()
            
            with open(self._credentials_path, 'w+') as fp:
                json.dump(pwd,fp)

        
    def connect(self):

        # load password
        with open(self._credentials_path,'r') as fp:
            pwd = json.load(fp)
        
        args = [self.host,'@'.join([self.user,self.host]),pwd,self.database]
        self._connection = pymssql.connect(*args)

        info('Connected to "%s" database @%s.'%(self.database,self.host))

    def query(self, qry):
        with self._connection.cursor() as cursor:
            cursor.execute(qry)
            self._result = cursor.fetchall()

    def execute_insert(self, statement):
        with self._connection.cursor() as cursor:
            cursor.execute(statement)
        self._connection.commit()

    
    @property
    def result(self):
        format_proxy = self.formaters['base']
        return format_proxy(self._result)

    @property
    def result_format(self):
        return 'base'

    @result_format.setter
    def result_format(self,tpl):
        ## TODO: Some checking is required here.
        self.formaters[tpl[0]] = tpl[1]
    

class ExampleConnector(BaseMSsqlDatabaseConnector):

    @property
    def host(self):
        return '<host-name>'

    @property
    def user(self):
        return '<username>'
    
    @property
    def database(self):
        return '<database-name>'

