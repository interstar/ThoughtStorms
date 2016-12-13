<?php
  // Minimal php script that forwards json files that are stored without a .json extension on another site
  // Can be used to turn a json export of another collection of documents, into something that the SFW client
  // can use.
  
  $url = "http://MY.DOMAIN.TLD/LONG/CONVOLUTED/PATH/";

  $path = $_SERVER["REQUEST_URI"];
  $word = substr($path,1);
  $word = str_replace(".json","",$word);

  $word = strtolower($word);
  if ($word != "") {
    $url .= $word;
  }

  $p = file_get_contents($url);

  echo $p;
?>
