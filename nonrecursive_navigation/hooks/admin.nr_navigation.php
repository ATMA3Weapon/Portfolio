<?php
/* This dynamic code hook (admin.visitor_stats) is loaded automatically into the controllers/controller.admin.session.true.inc.php file by the following code:
  foreach ($GLOBALS['hooks']->load('admin.'.strtolower($_GET['name'])) as $hook) include $hook;
  The purpose of this code is to make the page output loaded from the navigation link  to show the page view stats
*/

// The line below prevents direct access to this file which may lead to a path disclosure vulnerability
if(!defined('CC_DS')) die('Access Denied');

// include the class file
require_once('modules'.CC_DS.'plugins'.CC_DS.'nonrecursive_navigation'.CC_DS.'class.nr_navigation.php');

// initiate the plugin class as $nonrecursive_navigation
$nonrecursive_navigation = new nonrecursive_navigation(null);

// Get the page content from the get_statistics function. $page_content is later assigned to the master template file for you
//$page_content = $nonrecursive_navigation->test();
