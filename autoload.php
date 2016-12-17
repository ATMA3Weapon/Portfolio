<?php
/*
 * Autoloader writen by eric blackburn ATMA
 *
 * 
 */

// im not sure if we have to do this anymore or not?
global $_LG;

// make the autoloader class
class autoload_config {

	// our json array after convert it
	private $json_array;

	// gui objects
	private $gui_includes = array(); 

	// auto constructor
	public function __construct($json_string) {
		// decode the json from the string  and input it into our local scope temp variable array
		$json_array = json_decode($json_string, True);

		// set the variable into the private variable.
		$this->json_array = $json_array;

		// call tree check and clean.our tree
		$this->tree_check($json_array);

		// lets include our autoload files.
		$this->tree_build();
	}
	
	// public function to view our config data
	public function view_config() {
		return $this->json_array;
	}
	
	// private function to check our json tree and run our types of data in the config
	private function tree_check($array) {
		// lets step through the array and spit out key/value pairs
		foreach ($array as $key=>$value) {

			// looking for our types of data to switch on
			switch($key) {

				// this is for proccessing the include data
				case "includes":
					$this->process_include($value);

				// this is for processing the CSS link data,  possibly obsolete for smarty templating
				case "css_links":
					//$this->process_css_links($value);

				// for proccessing JS links, possibly obsolete for smarty templating
				case "js_links":
				
			}
		}
		
	}
	
	// we build the GUI folder file data and put it into the private GUI virtual DOM
	private function add_include($folder, $file) {

		//local private variable in the class add it
		$this->gui_includes[] = ($folder."". $file);
	}
	
	// this function goes through the list 
	private function process_include($include_array) {

		// we go through the array of includes to proccess
		foreach ($include_array as $key=>$value) {
			//switch set for our keys on what commands to do
			switch ($key) {

				// run ni the order of the list set.
				case "order":

					// run through the list and generate our command tree.
					foreach ($value['files'] as $keys2=>$values2) {
						$this->add_include($value['folder'], $values2);
					}
			}
		}
	}
	
	// we can finally run through our virtualized data structure and include each thing as we intended.
	private function tree_build() {
		// lets include the functional files.
		foreach ($this->gui_includes as $includes) {
			include $includes;
		}
	}
	
}

// our config file location
$config_file_name = "configs/conf.main.json";

// open it up and read it
$config_file_open = fopen($config_file_name, "r"); 

// spit out our data.
$config_file_content = fread($config_file_open, filesize($config_file_name));
fclose($config_file_open); // destroy

// this is our Landing gear virtual object.
$_LG['Config'] = json_decode($config_file_content, True);

// create and store our fancy new auto load config object.
$autoload_conf_obj = new autoload_config($config_file_content);

