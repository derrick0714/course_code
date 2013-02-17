<?php
$host = "localhost"; 
$user = "web_search"; 
$pass = "dengxu_wangqi"; 
$db   = "web_search_engine";

$conn = mysql_connect($host, $user, $pass);

if (!$conn)
{
    echo "Could not connect to server\n";
    exit();
} 

mysql_select_db($db,$conn);

$sql = "SELECT * FROM  `configuation`";


$result = mysql_query($sql);
if (!$result) 
{
    echo 'Could not run query: ' . mysql_error();
    exit;
}

$row = mysql_fetch_array($result);

$sql = "SELECT * FROM  `key_words`";
$result = mysql_query($sql);


?>


    <div class="my_span"></div>
	<div class="my_content">

    
	<div class="my_content">
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Seed:</b></th>
		    </tr>
		  </thead>
		  <tbody>

		    <tr>
		      <td width="200"><b>  result count : </b></td>
		      <td> <input type="text" name="result_count" value="10"></td>
		  	</tr>
		</div>
		 <div class="my_span"></div>
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Downloader:</b></th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <td width="200"><b>  thread num: </b></td>
		      <td>  <input type="text" name="down_thread" value="1"></td>

		    </tr>
		    <tr>
		      <td>download folder:</td>
		      <td>./data</td>

		    </tr>
		  </tbody>
		</table>	
	</div>
	<div class="my_span"></div>
	<div class="my_content">
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Parser:</b></th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <td width="200"><b>  thread num: </b></td>
		      <td> <input type="text" name="parse_thread" value="1"></td>
		    </tr>
		</table>	
	</div>
	
	<div class="my_span"></div>
	<div class="my_content">
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Seed:</b></th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <td width="200"><b>  key words : </b></td>
		      <td> <?=$row['seed_keywords']?></td>
		    </tr>
		    <tr>
		      <td width="200"><b>  result count : </b></td>
		      <td> <?=$row['seed_resultnum']?></td>
		    </tr>
		    <?php 
		    		$i=1;
		    		while ($array = mysql_fetch_array($result))
					{
						echo  "<tr><td width='200'>".$i++."</td> <td>".$array['url']."</td></tr>";			
					}
		    ?>	
	</div>

 </div>



<?php

mysql_close();

?>
