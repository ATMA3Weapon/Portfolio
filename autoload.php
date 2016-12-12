<?php
/*
 * Autoloader writen by eric blackburn ATMA
 * 

 * 
 */
global $_LG;

class autoload_config {
	private $json_array;
	private $gui_includes = array(); 

	public function __construct($json_string) {
		$json_array = json_decode($json_string, True);
		$this->json_array = $json_array;
		$this->tree_check($json_array);
		$this->tree_build();
	}
	
	public function view_config() {
		return $this->json_array;
	}
	

	private function tree_check($array) {
		foreach ($array as $key=>$value) {
			switch($key) {
				case "includes":
					$this->process_include($value);
				
				case "css_links":
					//$this->process_css_links($value);
				
				case "js_links":
				
			}
		}
		
	}
	
	private function add_include($folder, $file) {
		$this->gui_includes[] = ($folder."". $file); 
	}
	
	// this function goes through the list 
	private function process_include($include_array) {
		foreach ($include_array as $key=>$value) {
			switch ($key) {
				case "order":
					foreach ($value['files'] as $keys2=>$values2) {
						$this->add_include($value['folder'], $values2);
					}
			}
		}
	}
	
	private function tree_build() {
		// first lets include the functional files.
		foreach ($this->gui_includes as $includes) {
			include $includes;
		}
	}
	
}

$config_file_name = "configs/conf.main.json";
$config_file_open = fopen($config_file_name, "r"); 

$config_file_content = fread($config_file_open, filesize($config_file_name));
fclose($config_file_open);

$_LG['Config'] = json_decode($config_file_content, True);


$autoload_conf_obj = new autoload_config($config_file_content);

