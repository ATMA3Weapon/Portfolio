<?php

global $_LG, $_POST, $_SESSION;

class LG_Auth {
	
	private $gui_template = 'dark';
	private $gui_template_url = '';
	
	private $_Authorized = False; // if 
	private $_LoginType = 0; // default 0: not authed, 1 = local login, 2 = google, 3 = facebook.
	
	
	public function __construct() {
		global $_LG, $_POST, $_GET, $_SESSION;
		
		$this->gui_template_url = "templates/". $this->gui_template;
		
		$_LoginBody = $this->Build_Login_Body();
		$_LG['Smarty']->assign("Login_Body", $_LoginBody);
		
		/*
		if (isset($_GET['ajax'])) {
			if ($_GET['ajax'] == "local_login") {
				
				echo "local_login asdfasdfasdfasdfasdf";
				print_r($_POST);
			}
		
		}
		print_r($_POST);
		echo "YES";
		//e/cho $_LoginBody;
		//Echo "------";
		*/
		
		/* The get stuff */
		if (isset($_GET)) {
			if (isset($_GET['p'])) {
				if ($_GET['p'] == "logout") {
					unset($_SESSION['Authorized']);
					setcookie("Authorized", "", time() - 3600);
					$_LG['Smarty']->assign("_AUTHORIZATION_LOGOUT", "True");
					$url_path = "https://". $_SERVER['SERVER_NAME'] . $_SERVER['PHP_SELF'];
					//echo $url_path;
					echo "<script>document.location = '". $url_path ."';</script>";
				}
			}
		}
		
		/* Set the post stuff */
		
		if (isset($_POST)) {
			//if (!isset($_SESSION['Authorized'])) {
				if ((isset($_POST['input_local_email'])) && (isset($_POST['input_local_pass']))) {
					$user = $_POST['input_local_email'];
					$pass = $_POST['input_local_pass'];
					//print_r($_POST);
					//echo "aaa";
					if ($this->Login_Check($user, $pass) == True) {
						$_SESSION['Authorized'] = True;
					}
					else {
						$_LG['Smarty']->assign("_AUTHORIZATION_FAILED", "True");
					}
				}
			//}
		}
		
		/* set up authorization */
		/*
		 * if (isset($_COOKIE['Authorized'])) {
			if (!isset($_SESSION['Authorized'])) { $_SESSION['Authorized'] = True; }
			
			$_LG['Smarty']->assign("_AUTHORIZED", "True");

		}*/
		if (isset($_SESSION['Authorized'])) {
			if (!isset($_COOKIE['Authorized'])) { setcookie("Authorized", True, time()+31622400); }
			
			$_LG['Smarty']->assign("_AUTHORIZED", "True");
			
			
		}
	}
	
	
	//public function 
	

	
	private function Build_Login_Body() {
		global $_LG, $_COOKIE;
		
		$output = '';
		$output .= $_LG['Smarty']->fetch($this->gui_template_url ."/login_body.tpl");
		
		return $output;
		
	}
	
	
	private function Login_Check($email, $pass) {
		global $_LG;
		
		$email = filter_var($email, FILTER_SANITIZE_EMAIL);
		
		$login_query = "SELECT * FROM lg_users WHERE email LIKE :emailtext LIMIT 1"; //"SELECT * FROM lg_users WHERE email = ':emailtext'"; //"SELECT * FROM lg_users"; //
		$args = array(
			":emailtext" => [$email, PDO::PARAM_STR]
		);
		$results = $_LG['db']->query($login_query, $args);

		if ($results != False) {
			
			$q_email    = $results[0]['email'];
			$q_password = $results[0]['password'];
			
			if ($email == $q_email) {
				if (password_verify($pass, $q_password)) {
					return True;
				}
			}
		}
		return False;
	}
	
	
	
}

$_LG['Classes']['LG_Auth'] = new LG_Auth();

?>
