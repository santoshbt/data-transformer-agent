import psycopg2
from psycopg2 import sql

class DatabaseUtil:
	def __init__(self, db_config):
		self.db_config = db_config
		try:
			self.connection = psycopg2.connect(**db_config)
		except Exception as e:
			print(f"Error connecting to the database: {e}")
			self.connection = None

	def schema_details(self, schema_name):
		cursor = None
		connection = self.connection
	
		if connection is None:
			raise ConnectionError("Database connection is not available")

		cursor = connection.cursor()
		schema_info_context = f"Database Schema: {schema_name}\n\n"

		cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (schema_name,))
		tables_list = cursor.fetchall()

		schema_info_context += "Tables:\n"
		try:
			for table in tables_list:
				table_name = table[0]
				schema_info_context += f"- {table_name}\n"

				# Adding columns and datatypes
				cursor.execute(
					"SELECT column_name, data_type FROM information_schema.columns "
					"WHERE table_schema = %s AND table_name = %s",
					(schema_name, table_name),
				)
				column_list = cursor.fetchall()

				for column in column_list:
					column_name, data_type = column
					schema_info_context += f"  Column: {column_name}, Data Type: {data_type}\n"

				cursor.execute(
					sql.SQL("SELECT * FROM {}.{} LIMIT 5").format(
						sql.Identifier(schema_name),
						sql.Identifier(table_name),
					)
				)
				sample_data = cursor.fetchall()
				schema_info_context += " Sample Data:\n"
				for row in sample_data:
					schema_info_context += f"  {row}\n"

		except Exception as e:
			print(f"Error fetching schema details: {e}")
			schema_info_context = f"Error fetching schema details: {str(e) or repr(e)}"
		finally:
			if cursor is not None:
				cursor.close()
			if connection is not None:
				connection.close()

		return schema_info_context

	def execute_query(self, query):
		try:
			connection = self.connection
			cursor = connection.cursor()
			cursor.execute(query)
			result = cursor.fetchall()
			connection.commit()
			return str(result)
		except Exception as e:
			print(f"Error executing query: {e}")
			return None
		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()
			

obj = DatabaseUtil({
	"host": "localhost",
	"dbname": "postgres",
	"user": "postgres",
	"password": "admin",
	"port": 5432
})

result = obj.schema_details("public")

with open("test_schema_details", "w") as f:
	f.write(result)
