<?php

class LG_Register {
	
	
	private $gui_template = 'dark';
	private $gui_template_url = '';
	
	private $_Authorized = False; // if 
	private $_LoginType = 0; // default 0: not authed, 1 = local login, 2 = google, 3 = facebook.
	
	public function __construct() {
		global $_LG, $_POST, $_GET, $_SESSION;
		
		$this->gui_template_url = "templates/". $this->gui_template;
		
		$_RegisterBody = $this->Build_Register_Body();
		$_LG['Smarty']->assign("Register_Body", $_RegisterBody);
		
		if (isset($_POST)) {
			if ( (isset($_POST['input_register_email'])) && (isset($_POST['input_local_register_pass'])) && (isset($_POST['input_local_register_pass_confirm'])) ) {
				
				$_email = filter_var($_POST['input_register_email'], FILTER_SANITIZE_EMAIL);
				$_pass1 = filter_var($_POST['input_local_register_pass'], FILTER_SANITIZE_STRING);
				$_pass2 = filter_var($_POST['input_local_register_pass_confirm'], FILTER_SANITIZE_STRING);
				if ((filter_var($_email, FILTER_VALIDATE_EMAIL)) && (strlen($_pass1) >= 6) && (strlen($_pass2) >= 6)) {
					
					$password = password_hash($_pass1, PASSWORD_BCRYPT, ['cost' => 12]);
					
					$register_string = "INSERT INTO lg_users (email, password) VALUES (:emailtext, :passwordtext)"; //"SELECT * FROM lg_users WHERE email LIKE :emailtext LIMIT 1"; //"SELECT * FROM lg_users WHERE email = ':emailtext'"; //"SELECT * FROM lg_users"; //
					$register_args = array(
						":emailtext" => [$_email, PDO::PARAM_STR],
						":passwordtext" => [$password, PDO::PARAM_STR]
					);
					
					$results = $_LG['db']->query($register_string, $register_args);
					
					$_LG['Classes']['Mail']->register_user($_email);
				}
			
			}
		}
		
	}
	
	
	private function Build_Register_Body() {
		global $_LG, $_POST, $_GET, $_SESSION;
		
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/register_body.tpl");
		//echo $output;
		return $output;
		
	}
	
	
}

$_LG['Classes']['LG_Register'] = new LG_Register();

?>
