Parts Implemented by Gokay Temizkan
===================================

Add Method
----------

*This is the method to insert new tuples into the tables.*

Python Side
~~~~~~~~~~~

First, create the rule for Flask for the add method to server.py as below:

	.. code-block:: python

		  app.add_url_rule("/tablename_add", methods=["GET", "POST"], view_func=views_g.tablename_add_page)
		  
Then, create an HTML file and an HTML form for the method:		  
		 
	.. code-block:: HTML

		...
		
		<form action="" method="post" name="tablename_add">
		  <div class="field">
			<label for="id" class="label">Attribute</label>
			<div class="control">
			  <input type="number" name="attribute" class="input"/>
			</div>
		  </div>
		  
		...
		 
		  <div class="field is-grouped">
			<div class="control">
			  <button class="button is-primary is-small">Add</button>
			</div>
		  </div>
		</form>
		
		...

Finally, implemend add function in your views.py file:

	.. code-block:: python

		def tablename_add_page():
	
			if request.method == "GET":
				return render_template(
					"tablename_add.html"
				)
			else:
				form_tablename_attribute = request.form["tablename_attribute"]
				
				...
				
				STATEMENTS = [ '''
							  INSERT INTO TABLENAME VALUES
								  (%s, ...); ''' % (form_tablename_attribute, ...)  ]
				
				url= DATABASE_URL
				with dbapi2.connect(url) as connection:
				   cursor = connection.cursor()
				   for statement in STATEMENTS:
					   cursor.execute(statement)
				
				   cursor.close()
				
				return redirect(url_for("tablename_page"))

		
