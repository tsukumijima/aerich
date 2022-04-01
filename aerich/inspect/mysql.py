from typing import List

from aerich.inspect import Column, Inspect


class InspectMySQL(Inspect):
    @property
    def field_map(self) -> dict:
        return {
            "int": self.int_field,
            "smallint": self.smallint_field,
            "tinyint": self.bool_field,
            "varchar": self.char_field,
            "longtext": self.text_field,
            "text": self.text_field,
            "datetime": self.datetime_field,
            "float": self.float_field,
            "date": self.date_field,
            "time": self.time_field,
            "decimal": self.decimal_field,
            "json": self.json_field,
            "longblob": self.binary_field,
        }

    async def get_all_tables(self) -> List[str]:
        sql = "select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=%s"
        ret = await self.conn.execute_query_dict(sql, [self.database])
        return list(map(lambda x: x["TABLE_NAME"], ret))

    async def get_columns(self, table: str) -> List[Column]:
        columns = []
        sql = "select * from information_schema.columns where TABLE_SCHEMA=%s and TABLE_NAME=%s"
        ret = await self.conn.execute_query(sql, [self.database, table])
        for row in ret[1]:
            columns.append(
                Column(
                    name=row["COLUMN_NAME"],
                    data_type=row["DATA_TYPE"],
                    null=row["IS_NULLABLE"] == "YES",
                    default=row["COLUMN_DEFAULT"],
                    pk=row["COLUMN_KEY"] == "PRI",
                    comment=row["COLUMN_COMMENT"],
                    unique=row["COLUMN_KEY"] == "UNI",
                    extra=row["EXTRA"],
                    length=row["CHARACTER_MAXIMUM_LENGTH"],
                    max_digits=row["NUMERIC_PRECISION"],
                    decimal_places=row["NUMERIC_SCALE"],
                )
            )
        return columns