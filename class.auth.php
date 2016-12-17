<?php
/*
  Writen by Eric (ATMA),
  this is autoloaded by the landing gear loader system and a simple first version
  auth system for basic functionality while in development.
 */

// still not entirely sure if i need this or not, havnt used PHP in a few versions.
global $_LG, $_POST, $_SESSION;

// our class auth name
class LG_Auth {
	
	// private variables
	private $gui_template = 'dark'; // default dark theme
	private $gui_template_url = ''; // template string url
	
	private $_Authorized = False; // if user is authed or not
	private $_LoginType = 0; // default 0: not authed, 1 = local login, 2 = google, 3 = facebook.
	
	// autoload constructor when created.
	public function __construct() {
		global $_LG, $_POST, $_GET, $_SESSION;
		
		// generate our default template directory path.
		$this->gui_template_url = "templates/". $this->gui_template;
		
		// generate our login HTML body.
		$_LoginBody = $this->Build_Login_Body();

		// call our smarty global storage and assign the template variable to the html data.
		$_LG['Smarty']->assign("Login_Body", $_LoginBody);
		
		/* //work in progress
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
			// check if p is set on our url parameters
			if (isset($_GET['p'])) {
				// check if p is set to logout string
				if ($_GET['p'] == "logout") {
					// unset the session data for authorization
					unset($_SESSION['Authorized']);

					// remove the autorization cookie
					setcookie("Authorized", "", time() - 3600);

					// set our template variable for logging out to true.
					$_LG['Smarty']->assign("_AUTHORIZATION_LOGOUT", "True");

					// our location path url to send the user home on.
					$url_path = "https://". $_SERVER['SERVER_NAME'] . $_SERVER['PHP_SELF'];
					//echo $url_path;

					// print it out and lets get out of here.
					echo "<script>document.location = '". $url_path ."';</script>";
				}
			}
		}
		
		/* Set the post stuff */
		if (isset($_POST)) {

			//if (!isset($_SESSION['Authorized'])) {

			// lets check if our login POST input feilds exist
			if ((isset($_POST['input_local_email'])) && (isset($_POST['input_local_pass']))) {

					// local set user and pass variables from our post data
					$user = $_POST['input_local_email'];
					$pass = $_POST['input_local_pass'];

					//print_r($_POST);
					//echo "aaa";

					// run our login check pass the user and pass local vars and if it is a valid login credentials
					if ($this->Login_Check($user, $pass) == True) {
						// set the user session as an autorized user
						$_SESSION['Authorized'] = True;
					}
					else {
						// user failed to login and pass smarty template variables for accessing the right template parts
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

		// we check if the user session has been authorized
		if (isset($_SESSION['Authorized'])) {
			// if the cookie isnt set we set it up
			if (!isset($_COOKIE['Authorized'])) { setcookie("Authorized", True, time()+31622400); }
			
			// set the smarty stuff
			$_LG['Smarty']->assign("_AUTHORIZED", "True");
		}
	}
	
	
	//public function 
	
	// build the HTML for our login body
	private function Build_Login_Body() {
		global $_LG, $_COOKIE;
		
		// lets output our smarty data from the template.
		$output = $_LG['Smarty']->fetch($this->gui_template_url ."/login_body.tpl");
		
		return $output;
	}
	
	// lets check the login credentials
	private function Login_Check($email, $pass) {
		global $_LG;
		
		// lets filter and sanitize the email.
		$email = filter_var($email, FILTER_SANITIZE_EMAIL);
		
		// create our login SQL query string.
		$login_query = "SELECT * FROM lg_users WHERE email LIKE :emailtext LIMIT 1"; //"SELECT * FROM lg_users WHERE email = ':emailtext'"; //"SELECT * FROM lg_users"; //

		// generate our arguments for our SQL query string
		$args = array(
			":emailtext" => [$email, PDO::PARAM_STR]
		);

		// return the results of the query
		$results = $_LG['db']->query($login_query, $args);

		// if valid results were returned on our query
		if ($results != False) {
			
			// the email returned
			$q_email    = $results[0]['email'];

			// the password returned
			$q_password = $results[0]['password'];
			
			// lets check it one last time
			if ($email == $q_email) {

				// verify the password is correct.
				if (password_verify($pass, $q_password)) {
					// we have a valid login user and pass credentials
					return True;
				}
			}
		}
		// the login check failed and lets return it.
		return False;
	}
	
	
	
}

// we set our virtual class dom up for the autoloader.
$_LG['Classes']['LG_Auth'] = new LG_Auth();

?>
