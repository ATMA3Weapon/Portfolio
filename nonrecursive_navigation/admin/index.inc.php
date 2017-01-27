<?php
/*
 * Admin page installer/loader
 * no database install necessiary it uses the existing catagory data.
 *  - Default values
 * - 
 * 
 * 
 */ 

// The line below prevents direct access to this file which may lead to a path disclosure vulnerability
if(!defined('CC_DS')) die('Access Denied');


// get the module config and set default values if no config file exists already
if(!$module_config = $GLOBALS['config']->get('nonrecursive_navigation')) {
	$module_config = array (
	
	/*
		'background_color' 	=> '#E0FF67',
		'border_color' 		=> '#990000',
		'text_color' 		=> '#0000FF',
		'status' 			=> false,
		'font_family' 		=> 'Georgia'
	*/
	);
	// Set the default config into the CubeCart_config table
	$GLOBALS['config']->set('nonrecursive_navigation','', $module_config);
}

// pull in the module class file (CC_DS) is the directory seperator constant
require_once('modules'.CC_DS.'plugins'.CC_DS.'nonrecursive_navigation'.CC_DS.'class.nr_navigation.php');

// initiate the class as $vistor_stats
$nonrecursive_navigation = new nonrecursive_navigation($module_config);

// assign the preview counter HTML to the template file
//$GLOBALS['smarty']->assign('COUNTER_PREVIEW',$vistor_stats->get_counter());

// This is the standard module code as outlines in exmple one of the hooks development guide
$module	= new Module(__FILE__, $_GET['module'], 'admin/index.tpl', true, false);
$module->fetch();
$page_content = $module->display();
