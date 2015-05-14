using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Data;
using System.Linq;

public class main3 : MonoBehaviour {
	public static int LevelSeedSize = 50;
	public static int LevelsToSeed = 4;
	public static int LevelsDestroyedToShow = 2; /// the number of levels shown destroyed in the background.
	public static float LevelRate = 0.05f;

	public static System.Random rand = new System.Random();

	//public static DataSet LevelData;

	public preload preloadscript;     

	public LoadeStuff SceneDataToLoad;


	public static GameObject LevelsGameObject;

	public Dictionary<int, int> rowcount = new Dictionary<int, int>();  // key: level number, value: number of rows for level to load.
	public Dictionary<int, int> rowcounter = new Dictionary<int, int>();  // key: level number, value: number of rows counted for level so far.
	public Dictionary<int, bool> checkinglevel = new Dictionary<int, bool>();


	public class LoadeStuff {

		//public Hashtable SceneStyles = new Hashtable();
		public static Dictionary<string, List<string>> SceneStyles = new Dictionary<string, List<string>>();
		public static DataSet LevelData = new DataSet("LevelData");
		//public static int TotalLevels = LevelData.Tables.Count;

		public DataSet LevelDataReturn() {
			return LevelData;
		}

		public LoadeStuff() {

			List<string> starts = new List<string>();
			starts.Add ("default_start");
			SceneStyles.Add ("starts", starts);

			List<string> defaults = new List<string>();
			defaults.Add ("default_0");
			defaults.Add ("default_1");
			defaults.Add ("default_2");
			defaults.Add ("default_3");
			defaults.Add ("default_4");
			defaults.Add ("default_5");
			SceneStyles.Add ("defaults", defaults);
		}

		//public object this[string key] {
			//get { return RtData(key); }
			//set	{ StData(key, value); }
		//}


		static int TotalLevels() { return LevelData.Tables.Count; }
		static int NextLevel() { 
			if (TotalLevels() == 0) { return 0; }
			else { return TotalLevels()+1; }
		}
		static int levelSize(int lvlnumber) {
			int retNumb;
			if (lvlnumber == 0) { retNumb = -1 * LevelSeedSize; }
			else {
				retNumb = -1 * (LevelSeedSize + (int)Math.Round (LevelSeedSize * LevelRate * lvlnumber)); //-1 * LevelSeedSize * LevelRate * lvlnumber;
			}
			
			return retNumb; //-1 * LevelSeedSize * (LevelRate * lvlnumber);
		}
		private static int NextUID(string TableName) {
			//LevelData = new DataSet("LevelData");
			int NumOfRows = (int)(LevelData.Tables[TableName].Rows.Count);
			if (NumOfRows == 0) { return 0; }
			else {
				var test = (int)(LevelData.Tables[TableName].Rows[NumOfRows-1]["UID"]) + 1;
				return test;
			}
			return 1;
		}

		static int Style2Id(string style) {
			List<string> StylesToList = SceneStyles.Keys.ToList<string>();

			return StylesToList.IndexOf (style);
		}
		static string Id2Style(int styleid) {
			List<string> StylesToList = SceneStyles.Keys.ToList<string>();
			IList<string> Indexed = StylesToList.AsReadOnly();

			return Indexed[styleid];
		}


		static string RandomizedScene(string style, int level, int blockid) { //, string styletype) {
			string rete;

			if (level == 0) {
				if (blockid == 0) {
					var indexScenes = SceneStyles["starts"].AsReadOnly();
					int randomID = rand.Next (0, SceneStyles["starts"].Count-1);

					rete = indexScenes[randomID];
				}
				else {
					var indexScenes = SceneStyles[style].AsReadOnly();
					int randomID = rand.Next (0, SceneStyles[style].Count-1);
					
					rete = indexScenes[randomID];
				}
			}
			else {
				var indexScenes = SceneStyles[style].AsReadOnly();
				int randomID = rand.Next (0, SceneStyles[style].Count-1);
				
				rete = indexScenes[randomID];
			}


			return rete;
		}
		static string RandomizedSceneStyleType(int level, int blockid) {
			List<string> StylesToList = SceneStyles.Keys.ToList<string>(); // turn it into a normal List
			IList<string> IndexedStylesList = StylesToList.AsReadOnly(); // make an IList 

			string ret;
			if (level == 0) {
				if (blockid == 0) {
					ret = IndexedStylesList[0];
				}
				else {
					int randomID = rand.Next (1, SceneStyles.Count-1);
					ret = IndexedStylesList[randomID];
				}
			}
			else {
				int randomID = rand.Next (1, SceneStyles.Count-1);
				ret = IndexedStylesList[randomID]; 
			}
			return ret;
		}
		public void AddNewLevelToDatabase() {
			int lvlnumber = NextLevel ();
			string lvlname = NextLevel().ToString ();

			GameObject go = new GameObject("Level "+ lvlname) as GameObject;
			go.transform.parent = LevelsGameObject.transform;
			go.transform.position = new Vector3(0,0,0);

			LevelData.Tables.Add (lvlname);

			LevelData.Tables[lvlname].Columns.Add ("UID",		typeof(int));
			LevelData.Tables[lvlname].Columns.Add ("BlockID",	typeof(int));
			LevelData.Tables[lvlname].Columns.Add ("SceneID",	typeof(int));
			LevelData.Tables[lvlname].Columns.Add ("SceneName",	typeof(string));
			LevelData.Tables[lvlname].Columns.Add ("Style",		typeof(string));
			LevelData.Tables[lvlname].Columns.Add ("Position",	typeof(Vector3));
			LevelData.Tables[lvlname].Columns.Add ("Width",		typeof(double));
			LevelData.Tables[lvlname].Columns.Add ("GameObject",typeof(GameObject)); 

			for (int ta = levelSize(lvlnumber); ta <= LevelSeedSize; ta++) { // fill that level with game data
				DataRow NewRow = LevelData.Tables[lvlname].NewRow();

				NewRow["UID"]     	 = NextUID(lvlname); 
				NewRow["BlockID"] 	 = ta;


				string SceneStyling = RandomizedSceneStyleType(lvlnumber, ta);
				string randomScene = RandomizedScene(SceneStyling, lvlnumber, ta); //, randomStyleType()); 


				NewRow["SceneID"]	 = Style2Id(SceneStyling);
				NewRow["SceneName"]		 = randomScene;
				NewRow["Style"]		 = SceneStyling;

				LevelData.Tables[lvlname].Rows.Add (NewRow);
			}
		}
		public void SetPosition(int level, int blockid, Vector3 position) {
			//LevelData.Tables[levelname].Rows[0].
		}
		public void SetWidth(int level, int row, double width) {
			string levelname = level.ToString ();
			LevelData.Tables[levelname].Rows[row]["Width"] = width;
		}
		public void SetGameObject(int level, int row, GameObject gameob) {
			string levelname = level.ToString ();
			LevelData.Tables[levelname].Rows[row]["GameObject"] = gameob;
		}
		public void EnvokeLevelScene(int level) {

			string levelname = level.ToString ();

			DataRow[] SelectedLevelRows = LevelData.Tables[levelname].Select("", "BlockID ASC");

			foreach (var row in SelectedLevelRows) {
				int blockid = (int)row["BlockID"];
				string style = (string)row["Style"];
				string name = (string)row["SceneName"];

				//AsyncLoadScene(level, blockid, style, name));

			}

		}

	}


	void LevelLoader(int level) {
		SceneDataToLoad.AddNewLevelToDatabase(); // everytime its envoked it creates a new level inside the dataset

		DataSet test = SceneDataToLoad.LevelDataReturn();
		string lvlname = level.ToString();

		DataRow[] SelectedLevelRows = test.Tables[lvlname].Select ("", "BlockID ASC");
		rowcount.Add (level, SelectedLevelRows.Count());
		rowcounter.Add (level, 0);
		preloadscript.setsteps (SelectedLevelRows.Count()+1);

		foreach (var row in SelectedLevelRows) {
			int uid = (int)row["UID"];
			int blockid = (int)row["BlockID"];
			string style = (string)row["Style"];
			string name = (string)row["SceneName"];

			StartCoroutine(AsyncLoadScene(uid, level, blockid, style, name));
		}
		checkinglevel.Add (level, true);
		StartCoroutine(CheckIfLoaded(level));
		//yield return true;
	}
	IEnumerator AsyncLoadScene(int uid, int level, int blockid, string style, string name) {

		AsyncOperation AsyncsLod = Application.LoadLevelAdditiveAsync(name);
		yield return AsyncsLod;

		GameObject temp = GameObject.Find ("scene_"+ name);
		GameObject lvl  = GameObject.Find ("Levels/Level "+ level.ToString());

		temp.name = blockid +": scene_"+ name;
		temp.transform.parent = lvl.transform;

		string devscript = @"Levels/Level "+ level.ToString() +"/"+blockid +": scene_"+ name +"/_Data";
		grabdata test = GameObject.Find (devscript).GetComponent<grabdata>();

		double width = (double)test.getwidth();
		SceneDataToLoad.SetWidth (level, uid, width);
		
		string place = @"Levels/Level "+ level.ToString() +"/"+blockid +": scene_"+ name;
		GameObject gameob = GameObject.Find(place);
		SceneDataToLoad.SetGameObject(level, uid, gameob);
		rowcounter[level]++;
		preloadscript.incsteps();
	}
	IEnumerator CheckIfLoaded(int level) {
		while (checkinglevel[level] == true) {
			if (rowcounter[level] >= rowcount[level]) { // do what ever to make scene happen
				PositionLevel(level);

				checkinglevel[1] = false;
				yield break;
				//yield return true;
			}
			else { // go to sleep and recheck
				yield return new WaitForSeconds(0.5f);
			}
		}

	}


	void PositionLevel(int level) {
		print ("position time");

		DataSet test = SceneDataToLoad.LevelDataReturn();
		string lvlname = level.ToString();
		
		DataRow[] SelectedLevelRows = test.Tables[lvlname].Select ("", "BlockID ASC");

		DataRow[] startblock = test.Tables[lvlname].Select ("BlockID = 0", "BlockID ASC");
		double startWidth = (double)startblock[0]["Width"];

		var tasdfad = SelectedLevelRows.Take (50).Reverse();

		float lastposition = ((float)startWidth / 2);
		foreach (var row in tasdfad) {
			GameObject blockObject = (GameObject)row["GameObject"]; 
			double blockWidth = (double)row["Width"];

			float nextxpos = (lastposition + ((float)blockWidth / 2));

			lastposition = nextxpos;
			Vector3 newposition = new Vector3((nextxpos * -1), 0, 0); 
			blockObject.transform.position = newposition; 
		}

		var grargf = SelectedLevelRows.Skip (51);
		
		lastposition = ((float)startWidth / 2);
		foreach (var row in grargf) {

			GameObject blockObject = (GameObject)row["GameObject"]; 
			double blockWidth = (double)row["Width"];
			
			float nextxpos = (lastposition + ((float)blockWidth / 2));
			
			lastposition = nextxpos;
			Vector3 newposition = new Vector3(nextxpos, 0, 0); 
			blockObject.transform.position = newposition; 
		}

		//string pathname = @"Prefabs/player/player";
		//GameObject Player   = Resources.Load<GameObject>(pathname);
		//Instantiate(Player, new Vector3(0, 20, 0), Quaternion.identity);

		//preloadscript.showit = false;
		preloadscript.enabled = false;
		GameObject loadingGameobject = GameObject.Find ("Loading_Scene"); 
		loadingGameobject.SetActive(false);
		//Destroy(loadingGameobject.gameObject);

		/*
		double startWidth = (double)testss[0]["Width"];
		float previous = 0;
		foreach (var row in SelectedLevelRows) {
			GameObject blockObject = (GameObject)row["GameObject"]; 
			double blockWidth = (double)row["Width"];

			float xpos = (((float)startWidth / 2) + ((float)blockWidth / 2));
			int blockID = (int)row["BlockID"];
			float nxpos = (xpos * (float)blockID);
			previous = xpos;

			Vector3 newposition = new Vector3(nxpos, 0, 0); 

			print (blockID + " : "+ previous +" : "+ nxpos);
			blockObject.transform.position = newposition; //new Vector3(xpos, 0, 0);
		}*/
	}

	void Start() {
		Application.LoadLevelAdditive("loading");


		preloadscript = GameObject.Find("Dev/Scripts").GetComponent<preload>();           //
		preloadscript.enabled = true;                                                     // turn on the loading screen
		//preloadscript.showit = true;
		 

		//--------------------------------------------//
		LevelsGameObject = GameObject.Find ("Levels");
		SceneDataToLoad = new LoadeStuff();

		LevelLoader(0);

		//
		//
		/*
		SceneDataToLoad = new LoadeStuff();

		SceneDataToLoad.AddNewLevelToDatabase(); // everytime its envoked it creates a new level inside the dataset
		DataSet test = SceneDataToLoad.LevelDataReturn();
		DataRow[] SelectedLevel1Rows = test.Tables["1"].Select ("", "BlockID ASC");
		rowcount.Add (1, SelectedLevel1Rows.Count());
		rowcounter.Add (1, 0);

		foreach (var row in SelectedLevel1Rows) {
			int uid = (int)row["UID"];
			int blockid = (int)row["BlockID"];
			string style = (string)row["Style"];
			string name = (string)row["SceneName"];

			StartCoroutine(AsyncLoadScene(uid, 1, blockid, style, name));
		}
		checkinglevel.Add (1, true);
		StartCoroutine(CheckIfLoaded(1));*/
	}

	void Update() {

	}
}

/*
public class main3 : MonoBehaviour {
	
	public int LevelSeedSize = 50;
	public int LevelsToSeed = 4;
	public int LevelsDestroyedToShow = 2; /// the number of levels shown destroyed in the background.
	public int LevelGrowthRate = 3;

	public float LevelRate = 0.05f;

	public Dictionary<string, List<string>> PreloadsScenes  = new Dictionary<string, List<string>>();
	public Dictionary<string, List<string>> PreloadsPrefabs = new Dictionary<string, List<string>>();
	//public OrderedDictionary PreloadsScenes = new OrderedDictionary();
	//public OrderedDictionary PreloadsPrefabs = new OrderedDictionary();
	
	
	// GameObjects -------------------------------
	private GameObject Scripts;                 //
	// -------------------------------------------
	private GameObject NPCOrginals;             //
	private GameObject NPCCopies;               //
	// -------------------------------------------
	private GameObject ScenesCopies;            //
	// -------------------------------------------
	private GameObject ScenesOrginalLevels;     //
	private GameObject ScenesOrginalStarts;     //
	// -------------------------------------------
	private GameObject WindowHUD;               //
	private GameObject WindowOverlay;           //
	private GameObject Levels;				    //
	// -------------------------------------------
	public preload preloadscript;               //
	// -------------------------------------------
	
	public static DataSet LevelData; // = new DataSet("LevelData");
	public System.Random rand = new System.Random();
	
	
	//public List<string> StyleTypes;
	/*



		/scenes/default/default_0
		/scenes/default/default_1
		/scenes/default/default_2
		/scenes/default/default_3
		/scenes/default/default_4
		/scenes/default/default_5

		/scenes/starts/default_start

		* /
	
	IEnumerator AsyncSceneLoader(string name, string type) {
		//print ("yep");
		AsyncOperation AsyncsLod = Application.LoadLevelAdditiveAsync(name);
		yield return AsyncsLod;
		
		GameObject PreloadedScene = GameObject.Find("scene_"+ name);
		
		if (type == "starts") { PreloadedScene.transform.parent = ScenesOrginalStarts.transform; }
		else { 
			GameObject TypeCheck = GameObject.Find(type);
			if (null == TypeCheck) { 
				GameObject go = new GameObject(type) as GameObject;
				go.transform.parent = ScenesOrginalLevels.transform;
			}
			GameObject Moveit = GameObject.Find("Scenes/Orginal/Levels/"+type);
			
			PreloadedScene.transform.parent = Moveit.transform;
		}
		
		PreloadedScene.SetActive (false);
		preloadscript.incsteps ();
	}
	IEnumerator AsyncPrefabLoader(string typer, string name, string preload) {
		string pathname = @"Prefabs/"+ preload +"/"+ typer +"/"+ name;
		
		GameObject TypeCheck = GameObject.Find(typer);
		if (null == TypeCheck) { 
			GameObject go = new GameObject(typer) as GameObject;
			go.transform.parent = NPCOrginals.transform;
		}
		GameObject Moveit = GameObject.Find("NPCs/Orginal/"+typer);
		GameObject prefab   = Resources.Load<GameObject>(pathname);
		GameObject instance = Instantiate(prefab) as GameObject;
		
		instance.transform.parent = Moveit.transform; //NPCOrginals.transform;
		instance.name = name;
		instance.SetActive (false);
		
		preloadscript.incsteps ();
		yield return true;
	}



	IEnumerator AsyncLoader() {    //(string name, string type) {

		AsyncOperation AsyncsLod; // = Application.LoadLevelAdditiveAsync(name);
		yield return true; // AsyncsLod;

		/*
		//print ("yep");
		AsyncOperation AsyncsLod = Application.LoadLevelAdditiveAsync(name);
		yield return AsyncsLod;
		
		GameObject PreloadedScene = GameObject.Find("scene_"+ name);
		
		if (type == "starts") { PreloadedScene.transform.parent = ScenesOrginalStarts.transform; }
		else { 
			GameObject TypeCheck = GameObject.Find(type);
			if (null == TypeCheck) { 
				GameObject go = new GameObject(type) as GameObject;
				go.transform.parent = ScenesOrginalLevels.transform;
			}
			GameObject Moveit = GameObject.Find("Scenes/Orginal/Levels/"+type);
			
			PreloadedScene.transform.parent = Moveit.transform;
		}
		
		PreloadedScene.SetActive (false);
		preloadscript.incsteps ();  * /
	}


	
	private static int NextUID(string TableName) {
		//LevelData = new DataSet("LevelData");
		int NumOfRows = (int)(LevelData.Tables[TableName].Rows.Count);
		if (NumOfRows == 0) { return 0; }
		else {
			var test = (int)(LevelData.Tables[TableName].Rows[NumOfRows-1]["UID"]) + 1;
			return test;
		}
		return 1;
	}

	string fetchName(string style, int id) {
		print (PreloadsScenes[style]);
		return (string)"abds"; // PreloadsScenes[style];
	}

	int randomScene() {
		int rInt = rand.Next(0, 5);
		return rInt;
	}
	
	string sceneStyle() {
		//int rInt = rand.Next(1, 1);
		return "default";
	}

	int levelSize(int lvlnumber) {
		int retNumb;
		if (lvlnumber == 1) { retNumb = -1 * LevelSeedSize; }
		else {
			retNumb = -1 * (LevelSeedSize + (int)Math.Round (LevelSeedSize * LevelRate * lvlnumber)); //-1 * LevelSeedSize * LevelRate * lvlnumber;
		}

		return retNumb; //-1 * LevelSeedSize * (LevelRate * lvlnumber);
	}

	// creates a level inside the dataset table 
	// it picks how big the level will be and what scenes to use along the level.
	void GenerateLevelData(int lvlnumber) { // Generates a single level of data and rough for now, later will feature ability to smooth styles into each other.
		string lvlname = "Level"+lvlnumber;

		LevelData.Tables.Add (lvlname);
		
		LevelData.Tables[lvlname].Columns.Add ("UID",		typeof(int));
		LevelData.Tables[lvlname].Columns.Add ("BlockID",	typeof(Int32));
		LevelData.Tables[lvlname].Columns.Add ("SceneID",	typeof(Int32));
		LevelData.Tables[lvlname].Columns.Add ("Name",		typeof(string));
		LevelData.Tables[lvlname].Columns.Add ("Style",		typeof(string));
		LevelData.Tables[lvlname].Columns.Add ("Position",	typeof(Vector3));
		LevelData.Tables[lvlname].Columns.Add ("Width",		typeof(float));
		LevelData.Tables[lvlname].Columns.Add ("GameObject",typeof(GameObject)); 

		for (int ta = levelSize(lvlnumber); ta <= LevelSeedSize; ta++) { // fill that level with game data
			DataRow NewRow = LevelData.Tables[lvlname].NewRow();
			
			NewRow["UID"]     	 = NextUID(lvlname); 
			NewRow["BlockID"] 	 = ta;


			if (ta == 0) { 
				if (lvlnumber == 1) {
					NewRow["Style"] = "starts";
					NewRow["SceneID"] = 0;
				}
				else {
					NewRow["Style"] = sceneStyle(); ;
					NewRow["SceneID"] = randomScene();
				}
			}
			else {
				NewRow["Style"] = sceneStyle(); 
				NewRow["SceneID"] = randomScene(); 
			}
			string newpath = "/Scenes/"+sceneStyle()+""; //"/Levels/"+ row["Style"].ToString() +"/scene_"+ PreloadsScenes[row["Style"].ToString()][ta];

			NewRow["Name"] = "";
			LevelData.Tables[lvlname].Rows.Add (NewRow);
		}
	}
	

	//object GetBlockPath(string style, string sceneid) {
	//IList test = PreloadsScenes[style].AsReadOnly();
	//	return PreloadsScenes[style][sceneid];
	//}
	
	
	// Use this for initialization
	void Start () {
		LevelData = new DataSet("LevelData");
		// load up loading screen
		Application.LoadLevelAdditive("loading");
		
		preloadscript = GameObject.Find("Dev/Scripts").GetComponent<preload>();           //
		preloadscript.enabled = true;                                                     // turn on the loading screen
		
		
		//// --------------------------------------------------------------------------------
		// GameObject to find for later use.                                              //  
		// Scripts GameObjects                                                            //
		Scripts       = GameObject.Find("Dev/Scripts");                                   //   
		//                                                                                //
		// NPC GameObjects                                                                //
		NPCCopies   = GameObject.Find("NPCs/Copies");                                     //
		NPCOrginals = GameObject.Find("NPCs/Orginal");                                    //
		//                                                                                //
		// Scene Level and Start GameObjects                                              //
		ScenesCopies        = GameObject.Find("Scenes/Copies");                           //
		ScenesOrginalLevels = GameObject.Find("Scenes/Orginal/Levels");                   //
		ScenesOrginalStarts = GameObject.Find("Scenes/Orginal/Starts");                   //
		//                                                                                //
		// Window Overlay stuff                                                           //
		WindowHUD     = GameObject.Find("Windows/HUD");                                   //
		WindowOverlay = GameObject.Find("Windows/Overlay");                               //
		//// --------------------------------------------------------------------------------
		
		// set it up to use
		List<string> starts   = new List<string>();
		List<string> defaults = new List<string>();
		//List<string> style1   = new List<string>();
		//List<string> style2   = new List<string>();
		//List<string> style3   = new List<string>();
		
		//PreloadList starts = new PreloadList();
		//PreloadList defaults = new PreloadList();
		
		// initialize any preload scenes we want to use in this.
		starts.Add ("default_start");
		PreloadsScenes.Add ("starts", starts);  // add the types of starts to the list
		
		defaults.Add ("default_0");
		defaults.Add ("default_1");
		defaults.Add ("default_2");
		defaults.Add ("default_3");
		defaults.Add ("default_4");
		defaults.Add ("default_5");
		PreloadsScenes.Add ("default", defaults);  //add the default scene types
		
		//List<string> Airplanes	= new List<string>();
		List<string> Cars			= new List<string>();
		List<string> Helicopters	= new List<string>();
		List<string> People			= new List<string>();
		//List<string> Projectiles	= new List<string>();
		
		Cars.Add ("Car_type1");
		Cars.Add ("Car_type2");
		Cars.Add ("Car_type3");
		Cars.Add ("Car_type4");
		PreloadsPrefabs.Add ("Cars", Cars);
		
		Helicopters.Add ("Helicopter_type1");
		Helicopters.Add ("Helicopter_type2");
		PreloadsPrefabs.Add ("Helicopters", Helicopters);
		
		People.Add ("People_type1");
		People.Add ("People_type2");
		People.Add ("People_type3");
		People.Add ("People_type4");
		PreloadsPrefabs.Add ("People", People);
		
		int totalRows = starts.Count + defaults.Count + Cars.Count + Helicopters.Count + People.Count; 
		preloadscript.setsteps (totalRows);                                               // set the number of steps for the loading window
		
		//seed level stuff
		for (int at = 1; at <= LevelsToSeed; at++) { // create the level
			string lvlname = "Level"+at;
			//AddLevelAndColumns(lvlname); 
			GenerateLevelData(at);
		}

		//draw level 1
		DataRow[] SelectLevel1Rows = LevelData.Tables["Level1"].Select("", "BlockID ASC");
		foreach (var row in SelectLevel1Rows) {
			StartCoroutine(AsyncLoader()); // BlockID: position in level, Style: what type of level style to use for this block, SceneID: which scene to use at block of the given style type, 
		//	print (row["BlockID"]);
		}


		/*
		foreach (var scenetypes in PreloadsScenes) { //iterate through the type of scenes
			//print (scenetypes[0]);
			foreach (var scene in scenetypes.Value) {
				StartCoroutine(AsyncSceneLoader(scene, scenetypes.Key));
			}
		}
		
		int prefabCounts = 0;
		foreach (var preloadtypes in PreloadsPrefabs) { //iterate through the type of scenes
			foreach (var preload in preloadtypes.Value) {
				StartCoroutine(AsyncPrefabLoader(preloadtypes.Key, preload, "NPC"));
			}
		}
		
		//seed level stuff
		for (int at = 1; at <= LevelsToSeed; at++) { // create the level
			string lvlname = "Level"+at;
			CreateLevel(lvlname); 
			
			for (int ta = (-1 * LevelSeedSize); ta <= LevelSeedSize; ta++) { // fill that level with game data
				DataRow NewRow = LevelData.Tables[lvlname].NewRow();
				
				NewRow["UID"]     	 = NextUID(lvlname); 
				NewRow["BlockID"] 	 = ta;
				if (ta == 0) { 
					NewRow["Style"] = "starts";
					NewRow["SceneID"] = 0;
				}
				else {
					NewRow["Style"] = sceneStyle(); 
					NewRow["SceneID"] = randomScene(); 
				}
				
				LevelData.Tables[lvlname].Rows.Add (NewRow);
			}
		}
		
		//create level from loaded scene parts.
		//DataRow[] SelectLevel1Rows = LevelData.Tables["Level1"].Select();
		
		//string basepath = "/Scenes/Orginal";
		
		//foreach (var row in SelectLevel1Rows) {
		
		
		//	print (row["BlockID"] + " : "+ row["SceneID"]+ " : "+ row["Style"]);
		//print (row["SceneID"].GetType());
		//string prefabpath = GetBlockPath(row["Style"].ToString(), row["SceneID"].ToString() );
		//string prefabpath;
		//if (Convert.ToInt32 (row["BlockID"].ToString()) != 0) {
		//	int sceneID = Convert.ToInt32 (row["SceneID"].ToString());
		//	prefabpath = basepath+ "/Levels/"+ row["Style"].ToString() +"/scene_"+ PreloadsScenes[row["Style"].ToString()][sceneID];
		//	print(prefabpath);
		//}
		//else {
		//	int sceneID = Convert.ToInt32 (row["SceneID"].ToString());
		//	prefabpath = basepath+ "/Starts/scene_"+ PreloadsScenes[row["Style"].ToString()][sceneID];
		//	print(prefabpath);
		//}
		
		//GameObject toop = GameObject.Find (prefabpath);
		
		//GameObject goop = new GameObject(prefabpath) as GameObject;
		
		//print (prefabpath); row["SceneID"]
		//row["SceneID"];
		//row["Style"];
		//PreloadsScenes[row["Style"]][row["SceneID"]]
		
		var toop = GameObject.Find ("/Scenes/Orginal/Levels/default");
		print (toop);
		//GameObject instance = Instantiate(toop) as GameObject;
		//print (PreloadsScenes[row["Style"]]);
		//}
		//GetBlockPath("default", 2);
		//print(SelectLevel1Rows.Length);		
		/ *
* /
		
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}*/
