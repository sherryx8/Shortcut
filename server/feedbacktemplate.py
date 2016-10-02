feedbackTemplate = """<html>
<head>
	<link rel= "stylesheet" type= "text/css" href = "../style/style.css">
    <meta charset="UTF-8">
    <title>feedBack</title>
</head>

<body>

<div class ="intro-header">
<h1> Wellesley College </h1>
</div>

{% for l in dict %}
<div class ="comments">
   <h2>{{l['name']}}</h2>
   <h3>Average Score: {{l['avg']}} </h3>
   <h3>Recent Comments</h3>
   {% for c in l['com'] %}
   <p> {{c}} <p>
   {% endfor %}
 </div>  
{% endfor %}
<br>
<p><a href = "/review.html"> write a review </a></p>
<p><a href = "/"> return home </a></p>

</body>
</html>
"""
