<?php
/* This code hook (controller.index.php) is loaded automatically into the controllers/controller.index.inc.php file by the following code:
  foreach ($GLOBALS['hooks']->load('controller.index') as $hook) include $hook;
  The purpose of this code is to loge the page load and parse the counter HTML into main.php template file if the macro {$VISITOR_STATS_COUNTER}
  exists.
*/

// The line below prevents direct access to this file which may lead to a path disclosure vulnerability
if(!defined('CC_DS')) die('Access Denied');

// include the class file
require_once('modules'.CC_DS.'plugins'.CC_DS.'nonrecursive_navigation'.CC_DS.'class.nr_navigation.php');

// initiate the plugin class as $vistor_stats
$nonrecursive_navigation = new nonrecursive_navigation(null);

// log the page view
//$nonrecursive_navigation->log();

// assign the counter widget thing to the main front end template
$GLOBALS['smarty']->assign('NR_NAVIGATION',$nonrecursive_navigation->get_nr_navigation());
