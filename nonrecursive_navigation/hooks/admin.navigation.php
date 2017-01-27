<?php
/* This code hook (admin.navigation) is loaded automatically into the admin/sources/element.navigation.inc.php file by the following code:
  foreach ($GLOBALS['hooks']->load('admin.navigation') as $hook) include $hook;
  The purpose of this code is to create a link to load the plugin page to show page view statistics.
*/

// The line below prevents direct access to this file which may lead to a path disclosure vulnerability
if(!defined('CC_DS')) die('Access Denied');

// include the class file
require_once('modules'.CC_DS.'plugins'.CC_DS.'nonrecursive_navigation'.CC_DS.'class.nr_navigation.php');

// initiate the plugin class as $vistor_stats
$nonrecursive_navigation = new nonrecursive_navigation(null);

// create a custom parent navigation category with one child link. You can always add a link to an existing parent category with an array_merge.
$nav_sections['nonrecursive_navigation'] = $nonrecursive_navigation->_language_strings['top_level_admin_menu'];
$nav_items['nonrecursive_navigation'] = array($nonrecursive_navigation->_language_strings['child_admin_menu'] => '?_g=plugin&amp;name=nonrecursive_navigation');
