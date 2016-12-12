var App_Ajax_Pipe = funciton () {


};

var app_object = function () {
	this.app_name = ""; // string the literal name of the app and used as a way to identify it
	this.app_uid = ""; // string the unique id name of the app and used as another way to identify it

	this.app_active = false; // bool if the is open on the users active on the devices landing gear page

	this.app_auth_token = "";// string the token given to this app from the server to allow users to make their next ajax and rest calls
	this.app_auth_token_expire = ""; // string the time when the token expires.

	this.app_config = "";//json the public config info saved in the object to store data

	this.app_css  = [];      //list the css files to apply to the header
	this.app_font = [];      //list fibt fukes
	this.app_images = [];    //list images
	this.app_js_files = [];  //list
	this.app_templates = []; // list names of the theme names

	this.app_index = ""; //
	this.app_settings = "";//
	this.app_menu = ""; //

	this.app_title = "";// string, change tab header string or return it

	this.app_icon_html = "";// string, change string to or return  it
	this.app_body_html = ""; // string, return or set the body html
	this.app_menu_html = "";// string, return or set menu html
	this.app_settings_html = ""; // string, retrn or set modal settings html

	this.app_events = ""; // events regisutered with this ap
	this.app_alerts = "";// new active alerts

	this.app_ajax_conduite = new App_Ajax_Pipe();
};

var lg_apps_array_object = function () {
	this.apps_array = {};

	this.app = {
		"weatherlg": new app_object(),
		"email": new app_object()

	};

	//this.add_app

	// consturctor

	//destructor

};

var lg_gold_object = function () {


}

var lg_ajax = function () {

};

var lg_object = function () {
	/*
	menu_button: new menu_button_object(),
	menu_body: new menu_body_object(),
	menu_favapps: new menu_favapps_object(),
	menu_appsbar: new menu_appsbar_object(),

	/*
	lg_signin:
	lg_signout:
	lg_register:
	lg_lostpass:
	*/

	//lg_device: new lg_device_object(),
	this.lg_apps = lg_apps_array_object();

};

lg_object.init();
lg_object.login(user, pass, token);

if (lg_object.logged() === True) {
	lg_object.gold.config();
	lg_object.menu_button.animation_type();
	lg_object.menu_button.animate_start();
	lg_object.menu.populate_fav_menu();
	lg_object.device.set();

}




