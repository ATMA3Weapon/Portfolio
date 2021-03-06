<?php
/*
 * 
 * LG gui by Eric Blackburn
 * auto loaded by the landing gear system and pushed into the landing gear virtual control dom.
 *
 *
 */ 
global $_LG;

// this is basically our entire view controller for our stuff.
class LG_Gui {
	
	// begin our private dom variables
	private $css_links = array(); //
	private $js_links = array();
	
	// our gui template name
	private $gui_template = 'dark';
	
	// our gui template directory path.
	private $gui_template_url = '';
	
	// gui body dom array
	private $gui_body = array();
	
	// different gui parts dom arrays
	private $gui_modals = array();
	private $gui_header = array();
	private $gui_window = array();
	
	// final bits
	private $GUI_array  = array(); // this is the complete body
	private $GUI_string = '';
	
	// more dom space.some may be possibly obsolete
	private $gui_Header = array();
	private $gui_JScripts = array();
	private $gui_Modal_Space = array();
	private $gui_Menu_Space = array();
	private $gui_Body_Space = array();
	private $gui_Golden_Space = array();
	private $gui_Footer_Space = array();

	//private $first_time = $_C
	
	// our construction function
	public function __construct() {
		global $_LG;
		
		// set the gui template directory.
		$this->gui_template_url = "templates/". $this->gui_template;

		 // lets build the dom array for holding our template data based on the config.
		$this->Build_CSS_Links_Array();

		// lets build the dom array for holding our JS links data based on the config.
		$this->Build_JS_Links_Array();
		
		// more array dom building
		$_Header		= $this->Build_Header();
		$_JScripts		= $this->Build_Jscripts();
		$_Modal_Space	= $this->Build_Modal_Space();
		$_Menu_Space	= $this->Build_Menu_Space();
		$_Body_Space	= $this->Build_Body_Space();
		$_Golden_Space	= $this->Build_Golden_Space();
		$_Footer_Space	= $this->Build_Footer_Space();
		
		// set all that to smarty template variables for our main body parts
		$_LG['Smarty']->assign("Header", $_Header);
		$_LG['Smarty']->assign("JScripts", $_JScripts);
		$_LG['Smarty']->assign("Modal_Space", $_Modal_Space);
		$_LG['Smarty']->assign("Menu_Space", $_Menu_Space);
		$_LG['Smarty']->assign("Body_Space", $_Body_Space);
		$_LG['Smarty']->assign("Golden_Space", $_Golden_Space);
		$_LG['Smarty']->assign("Footer_Space", $_Footer_Space);

		//$_LG['Smarty']->display($this->gui_template_url ."/index.tpl");
		
	}
	
	// return the current template directory
	public function Get_Template_URL() {
		return $this->gui_template_url;
	}

	// return the current template name
	public function Get_Template_Name() {
		return $this->gui_template;
	}
	
	// build the CSS links virtual dom
	private function Build_CSS_Links_Array() {
		// global Landing gear tools
		global $_LG;
		
		// lets call up out config, which css links, and their order
		$order_data = $_LG['Config']['css_links']['order'];

		// loop through the data by type and spit out the data.
		foreach ($order_data as $type=>$data) { //folders / urls ordering

			// our command is a folders type.
			if ($type == "folders") {

				// run through the list of folders.
				foreach ($data as $folders=>$files) {

					// run through each of the files in each folder.
					foreach ($files as $order=>$tpl_data) {

						// now loop through each indvidual item and slam it into our CSS virutal dom.
						foreach ($tpl_data as $key=>$file) {

							// our locally stored css links dom. spit out the folders path and file name. and place the string in the array list.
							$this->css_links[$order] = [$key=>$folders.$file];
						}
					}
				}
			}
			// switch out to url based links instead of a directory/file
			if ($type ==  "urls") {

				// go through each file list
				foreach ($data as $order=>$url) {

					// go through them
					foreach ($url as $key=>$file) {

						// slam it into oru virtual dom too.
						$this->css_links[$order] = [$key=>$url[$key]];
					}
				}
			}
		}

		// lets sort the dom
		ksort($this->css_links);
		//print_r($this->css_links);
	}
	
	// les build the JS virtual dom
	private function Build_JS_Links_Array() {
		global $_LG;
		
		// return the config for js links and their order.
		$order_data = $_LG['Config']['js_links']['order'];

		// the same as above
		foreach ($order_data as $type=>$data) { //folders / urls ordering
			if ($type == "folders") {
				foreach ($data as $folders=>$files) {
					foreach ($files as $order=>$tpl_data) {
						foreach ($tpl_data as $key=>$file) {
							$this->js_links[$order] = [$key=>$folders.$file];
						}
					}
				}
			}
			if ($type ==  "urls") {
				foreach ($data as $order=>$url) {
					foreach ($url as $key=>$file) {
						$this->js_links[$order] = [$key=>$url[$key]];
					}
				}
			}
		}
		ksort($this->js_links);
		//print_r($this->js_links);
	}
	
	// lets build the header.virutal dom
	private function Build_Header() {
		global $_LG;
		
		//output string
		$output = '';
		
		//Meta lets assign the meta html to the smarty template
		$meta = '';
		$_LG['Smarty']->assign("Meta", $meta);
		
		//Auth authorization smarty template
		$auth = '';
		$_LG['Smarty']->assign("Auth", $auth);
		
		//Page_Title smarty template
		$page_title = '';
		$_LG['Smarty']->assign("Page_Title", $page_title);
		
		//CSS_Space creation
		$css_output = '';

		// use the virtual css link data to the output html and smarty templates
		foreach ($this->css_links as $csslinks_data) {

			//lets loop thrugh it and fill this up
			foreach ($csslinks_data as $target=>$value) {

				// assign smarty template target and value for our page. auto load the header.
				$_LG['Smarty']->assign($target, $value);

				// compile up and add our smarty html into our css string output
				$css_output .= $_LG['Smarty']->fetch($this->gui_template_url ."/". $_LG['Config']['css_links']['tpl_file']); 
			}
			
		}
		// assign our template data to our smarty variable
		$_LG['Smarty']->assign("CSS_Space", $css_output);

		// our header html output
		$output  = $_LG['Smarty']->fetch($this->gui_template_url ."/header.tpl");
		
		return $output; // output it all
	}

	// build javascript head data for the page.
	private function Build_Jscripts() {
		global $_LG;
		
		// set up our initial string variable to add to
		$output = '';

		// loop through the JS virtual dom and create our actual html data for output.
		foreach ($this->js_links as $csslinks_data) {
			// more loops
			foreach ($csslinks_data as $target=>$value) {

				// assign our javascript data.
				$_LG['Smarty']->assign($target, $value);

				// put our output string data. festch template data
				$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/". $_LG['Config']['js_links']['tpl_file']); 
			}
		}
		
		// output our javascript
		return $output;
	}

	// our modal space for different applications.
	private function Build_Modal_Space() {
		global $_LG;
		
		// our output string, not
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/lg_modal_body.tpl"); 
		
		return $output;
		
	}

	// menu space
	private function Build_Menu_Space() {
		global $_LG;
		
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/lg_menu_body.tpl"); 
		
		return $output;
		
	}

	/// body space
	private function Build_Body_Space() {
		global $_LG;
		
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/lg_window_body.tpl"); 
		
		return $output;
		
	}

	// golden layout ordered space
	private function Build_Golden_Space() {
		global $_LG;
		
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/lg_golden_body.tpl"); 
		
		return $output;
	}
	
	private function Build_Footer_Space() {
		global $_LG;
		
		$output = '<!-- more on this later-->';
		//$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/lg_window_body.tpl"); 
		
		return $output;
		
	}

}

// set up our autoload stuff.
$_LG['Classes']['LG_Gui'] = new LG_Gui();


?>
