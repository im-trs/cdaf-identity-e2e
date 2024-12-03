# PyOdbc Install on Mac
 
### Install with homebrew
Running:
> brew install unixodbc 
> 
> pip install --no-binary :all: pyodbc

https://github.com/mkleehammer/pyodbc

issue on Mac M1 Apple Silicon:
https://github.com/mkleehammer/pyodbc/issues/1124

### Created symbolic links
https://stackoverflow.com/questions/44527452/cant-open-lib-odbc-driver-13-for-sql-server-sym-linking-issue?rq=1

Running:
> odbcinst -j
> 
> sudo ln -s /opt/homebrew/etc/odbcinst.ini /etc/odbcinst.ini
> 
> sudo ln -s /opt/homebrew/etc/odbc.ini /etc/odbc.ini


### Install MSSQL Driver
> brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
> 
> brew update
> 
> ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
> 
> view /opt/homebrew/etc/odbcinst.ini

### PyCharm Database
> view > tools windows > database
> Click on 
>> new > datasource > Microsoft SQL Server
> Further steps: https://www.jetbrains.com/help/pycharm/microsoft-sql-server.html