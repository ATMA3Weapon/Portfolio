<?php
// This file contains all the main functions for the plugin all nice and tidy in its own class
class nonrecursive_navigation {
	
	// This variable stores the module configuration data
	public $_module_config = array();
	// This variable contains the language strings in the language/module.definitions.xml file
	public $_language_strings = array();
	
	//private $_tree_data = array();
	public $newtree = array();
	
	
	public function __construct($module_config = null) {
		// Set the module config
		$this->_module_config = is_array($module_config) ? $module_config : $GLOBALS['config']->get('nonrecursive_navigation');
		
		// Load the module language strings using the language class
		$GLOBALS['language']->loadDefinitions('nonrecursive_navigation', 'modules/plugins/nonrecursive_navigation/language', 'module.definitions.xml');
		$this->_language_strings = $GLOBALS['language']->getStrings('nonrecursive_navigation');
		
		$tree_data = $GLOBALS['catalogue']->getCategoryTree();
		$this->newtree = $tree_data;
		$this->nr_modify_tree($this->newtree, 0);

		$nr_new_nav = $this->nr_navigation_builder($this->newtree);
		$GLOBALS['smarty']->assign('NR_NAV_TREE', $nr_new_nav);

		//print_r($this->newtree);
	}

	
	private function nr_modify_tree(&$array, $level = 0) {
		foreach ($array as $key => $value) {
			if (is_array($array[$key])) {
				$level++;
				$this->nr_modify_tree($array[$key], $level);
				$level--;
			} 
			else if(!isset($array['depth'])) {
				$array['depth'] = $level;
				
			}			
		}
		
	}

	
	public function display_nr_navigation() {
		$tree_data = $GLOBALS['catalogue']->getCategoryTree();
		
		$GLOBALS['smarty']->assign('NR_NAV', $branch);
	}
	
	private function nr_navigation_builder($tree) {
		$out = '';
		$GLOBALS['gui']->changeTemplateDir('modules/plugins/nonrecursive_navigation/skin/');
		
		if (is_array($tree)) {
			foreach ($tree as $branch) {
				if (isset($branch['children'])) {
					$branch['children'] = $this->nr_navigation_builder($branch['children']);
				}
				$branch['url'] = $GLOBALS['seo']->buildURL('cat', $branch['cat_id'], '&');
				$GLOBALS['smarty']->assign('BRANCH', $branch);
				//foreach ($GLOBALS['hooks']->load('class.gui.display_navigation.make_tree') as $hook) include $hook;
				//echo "brn:". $branch['depth'];
				if ($branch['depth'] <= 1) {
					$out .= $GLOBALS['smarty']->fetch('modules/plugins/nonrecursive_navigation/skin/navigation_top.tpl');
				}
				else if ($branch['depth'] > 1) {
					$out .= $GLOBALS['smarty']->fetch('modules/plugins/nonrecursive_navigation/skin/navigation_sub.tpl');
				}
			}
			
		}
		
		$GLOBALS['gui']->changeTemplateDir();
		
		return $out;
			
	}
	
	
	
	// This function gets the counter html from the skin/counter.tpl file
	public function get_nr_navigation() {
		// Tell the GUI class to look in the correct directory
		$GLOBALS['gui']->changeTemplateDir('modules/plugins/nonrecursive_navigation/skin/');
		// assign the module config, page views and language strings
		$GLOBALS['smarty']->assign('MODULE_CONFIG',$this->_module_config);
		$GLOBALS['smarty']->assign('PAGE_VIEWS',$this->_count_views());
		$GLOBALS['smarty']->assign('MODULE_LANG',$this->_language_strings);
		// Fetch the HTML to return in the function
		$html_out = $GLOBALS['smarty']->fetch('counter.tpl');
		// Function below resets Template dir. This is crucial for stanard template files loaded after this!
		$GLOBALS['gui']->changeTemplateDir();
		return $html_out;
	}


	
	// This private function can only be accessed from within this class. It returns a total count of page views
	private function _count_views() {
		$data = $GLOBALS['db']->misc("SELECT SUM(page_views) as `total_page_views` FROM `plugin_visitor_stats`;");
		return (int)$data[0]['total_page_views'];
	}
	
	
	

}
?>
