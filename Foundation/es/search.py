from tools import client

response = client.esql.query(
	query="""
    	FROM book
        	| LIMIT 5
    	""",
	format="csv"
)

print(response)
