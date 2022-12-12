class DataBaseTable:
    class DataTypes:
        """
        data types consts
        """
        INT = "INT"

    def __init__(self, title, columns):
        """
        represent a db table
        :param title: the title of the table
        :param columns: list of all the table columns, each column is represented by a tuple of (name, Type)
        """

        self.__title = title
        self.__columns = columns

    @property
    def sql_cmd_open_or_create_table(self):
        """
        get the sql cmd to open or create the table
        :return:
        """

        columns_txt = ", ".join([" ".join(column) for column in self.__columns])
        return f"CREATE TABLE if not exists {self.__title} ({columns_txt})"
        # we may want to use "OPEN OR CREATE"

    def sql_cmd_insert(self, data):
        """
        get the sql cmd to add new data into the file
        :param data: the data to insert as lst of the data at the order of columns
        :return: None
        """

        columns_names = ", ".join([title for (title, _) in self.__columns])
        values_txt = ", ".join(data)
        return f"INSERT INTO {self.__title}({columns_names}) VALUES ({values_txt})"


if __name__ == '__main__':
    t = DataBaseTable("TestTable", [
        ("c1", "Type1"),
        ("c2", "Type2")
    ])
    print(t.sql_cmd_open_or_create_table)
    print(t.sql_cmd_insert(["d1", "d2"]))
