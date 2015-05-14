using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Data;
using System.IO;
using System.Xml;
using System.Security.Cryptography;
using System.Text;

public class xdbe20 : MonoBehaviour {
	public class Database {
		public static string DBName;
		private static Stream DBSchema;
		private static DataSet DBSet = new DataSet();  // Stores tables under here as a dataset for manipulation.
		private static string DBFileLocation;
		private static FileStream DBFileStream;  // the physical filestream for the datafile storage.

		private static bool DBEncryption = true;       // Encyrption is automatically enabled.
		private static bool DBLocalFileDatabase = false;      // DBDataFile if enabled it switches the database to look to local game files.
		
		public QuerySystem Query; // = new QuerySystem();
		public UserPrefsSystem UserPrefs; // = new UserPrefsSystem();

		//////////////////////////////////////
		///// class overload values      /////
		//////////////////////////////////////
		public Database(string Name, bool LocalGameFile) {
			if (LocalGameFile == true) { DBLocalFileDatabase = true; }
			else { DBLocalFileDatabase = false; }

			DBName = Name;
			DBFileLocation = DbFileLocation();

			LoadDatabase();

			//print (LocalGameFile);
			//print (DBFileLocation);
		}
		public Database(string Name, bool LocalGameFile, bool Encryption) {
			if (LocalGameFile == true) { DBLocalFileDatabase = true; }
			else { DBLocalFileDatabase = false; }

			if (Encryption == true) { DBEncryption = true; }
			else { DBEncryption = false; }

			DBName = Name;
			DBFileLocation = DbFileLocation();

			LoadDatabase();

			//print (DBFileLocation);
		}
		public Database(string Name, bool LocalGameFile, bool Encryption, bool UsrPrfsOn) {
			if (LocalGameFile == true) { DBLocalFileDatabase = true; }
			else { DBLocalFileDatabase = false; }
			
			if (Encryption == true) { DBEncryption = true; }
			else { DBEncryption = false; }

			if (UsrPrfsOn == true) { UserPrefs = new UserPrefsSystem(); }

			DBName = Name;
			DBFileLocation = DbFileLocation();
			
			LoadDatabase();
			
			//print (DBFileLocation);
		}
		//////////////////////////////////////
		///// Add Stuffs Datatable       /////
		//////////////////////////////////////
		static bool AddTable(string TableName) {
			if (DBSet.Tables.Contains (TableName) == false) { 
				DBSet.Tables.Add(TableName);
				DBSet.Tables[TableName].Columns.Add ("UID", typeof(int));
				return true;
			}
			else {
				return false;
			}

			SaveDatabase ();
		} 
		static bool AddColTo(string TableName, string ColName, Type ColDataType) {
		
			if (DBSet.Tables[TableName].Columns.Contains (ColName) == false) {
				DBSet.Tables[TableName].Columns.Add (ColName, ColDataType);
				SaveDatabase ();
				return true;
			}
			else {
				return false;
			}
		}
		static void AddRowTo(string TableName,  Hashtable RowData) { 
			DataRow NewRow = DBSet.Tables[TableName].NewRow();
			NewRow["UID"] = NextUID(TableName); 
			foreach (DictionaryEntry dictionaryEntry in RowData) { NewRow[dictionaryEntry.Key.ToString()] = dictionaryEntry.Value; }
			DBSet.Tables[TableName].Rows.Add (NewRow);
			SaveDatabase ();
		}

		//////////////////////////////////////
		///// sstufffss                  /////
		//////////////////////////////////////
		static void LoadDatabase() { 
			if (!File.Exists(DbFileLocation())) { Stream CreateFile = File.Create(DbFileLocation()); CreateFile.Close ();}

			StreamReader temp = new StreamReader(DbFileLocation());  //open file
			string trimstream = temp.ReadToEnd().ToString(); //.Length;


			print ("1 "+ trimstream.Length);
			if (trimstream.Length != 0) {
				print ("2");
				StringReader XMLOutput; // = new StringReader(CryptXML);

				if (DBEncryption == true) {
					string CryptXML = Dnc("12345678901234567890123456789012", trimstream); 
					XMLOutput = new StringReader(CryptXML);
				}
				else {
					XMLOutput = new StringReader(trimstream);
				}

				print (XMLOutput);
				DBSet.ReadXml(XMLOutput); // read XML from file and set it to the dataset
			}
		}
		static void SaveDatabase() {
			StringWriter XMLStream = new StringWriter(); // create a stream 

			DBSet.WriteXml(XMLStream, XmlWriteMode.WriteSchema); // Write XML data including schema to string writer

			string XMLString = XMLStream.ToString();
			string XMLOutput;

			if (DBEncryption == true) {
				string CryptXML = Enc("12345678901234567890123456789012", XMLString);
				XMLOutput = CryptXML.ToString().Trim ();
			}
			else {
				XMLOutput = XMLString;
			}

			StreamWriter XMLWriter = new StreamWriter(DbFileLocation()); 
			XMLWriter.WriteLine(XMLOutput);
			XMLWriter.Close();
		}



		//////////////////////////////////////
		///// static returning variables /////
		//////////////////////////////////////
		static string DbFileLocation() { 
			string datapath;

			if (DBLocalFileDatabase == true) { datapath = Path.Combine (Application.dataPath, @""+ DBName +".xdbe"); }
			else { datapath = Path.Combine (Application.persistentDataPath, @"databases\"+ DBName +".xdbe"); }

			datapath = datapath.Replace ("/", "\\"); 

			return datapath;
		}	

		static int NextUID(string TableName) {
			int NumOfRows = (int)(DBSet.Tables[TableName].Rows.Count);
			if (NumOfRows == 0) { return 0; }
			else {
				var test = (int)(DBSet.Tables[TableName].Rows[NumOfRows-1]["UID"]) + 1;
				return test;
			}
			return 1;
		}

		static string Enc(string key, string datatocrypt) {
			byte[] KeyArray = UTF8Encoding.UTF8.GetBytes (key);
			byte[] CryptArray = UTF8Encoding.UTF8.GetBytes (datatocrypt);
			
			RijndaelManaged rijCrypt = new RijndaelManaged();
			
			rijCrypt.Key = KeyArray;
			rijCrypt.Mode = CipherMode.ECB;
			
			rijCrypt.Padding = PaddingMode.PKCS7;
			
			ICryptoTransform CryptTransform = rijCrypt.CreateEncryptor();
			
			byte[] CryptResult = CryptTransform.TransformFinalBlock (CryptArray, 0, CryptArray.Length);
			
			return Convert.ToBase64String (CryptResult, 0, CryptResult.Length);
		}

		static string Dnc(string key, string datatocrypt) {
			byte[] KeyArray = UTF8Encoding.UTF8.GetBytes (key);
			byte[] CryptArray = Convert.FromBase64String (datatocrypt); 
			
			RijndaelManaged rijCrypt = new RijndaelManaged();
			
			rijCrypt.Key = KeyArray;
			rijCrypt.Mode = CipherMode.ECB;
			
			rijCrypt.Padding = PaddingMode.PKCS7;
			
			ICryptoTransform cTransform = rijCrypt.CreateDecryptor ();
			
			byte[] CryptResult = cTransform.TransformFinalBlock (CryptArray, 0, CryptArray.Length);
			
			return UTF8Encoding.UTF8.GetString (CryptResult);
		}	
			
			
		//////////////////////////////////////
		///// Query system               /////
		//////////////////////////////////////
		public class QuerySystem {
			public object Select(string TableName, string expression = null, string sortexpression = null) {//string OrderBy=null, string WhereAt=null, string ColSelects=null) {
				var res = DBSet.Tables[TableName].Select(expression, sortexpression);
				return res;
			}
			public object Insert(string TableName, Hashtable RowData) { 
				AddRowTo(TableName, RowData); 
				return true;
			}
			public object Update(string TableName, Dictionary<int, Hashtable> RowData) {
				foreach (KeyValuePair<int, Hashtable> row in RowData) {
					int i = row.Key;
					foreach (DictionaryEntry dat in row.Value) {
						DBSet.Tables[TableName].Rows[i][dat.Key.ToString()] = dat.Value;
					}
				}
				SaveDatabase ();
				
				return true;
			}
			public object Remove(string TableName, int RowId) { 
				// delete row at id line
				DBSet.Tables[TableName].Rows[RowId].Delete ();
				SaveDatabase ();
				return true;
			}
			public object NewTable(string TableName) { 
				AddTable(TableName);
				return true;
			}
			public object NewColumnTo(string TableName, Hashtable Columns) {  
				foreach (DictionaryEntry dat in Columns) { 
					AddColTo (TableName, dat.Key.ToString (), dat.Value.GetType ());
				}
				
				return true;
			} 
			public object DeleteTable(string TableName) { 
				DBSet.Tables.Remove (TableName);
				return true;
			}
			public object DeleteColumnTo(string TableName, List<string> Columns) {
				foreach (string dat in Columns) { 
					DBSet.Tables[TableName].Columns.Remove (dat);
				}
				SaveDatabase();
				return true;
			}
			public object DeleteRowTo(string TableName, int RowId) { 
				// delete row at id line
				DBSet.Tables[TableName].Rows[RowId].Delete ();
				SaveDatabase ();
				return true;
			}
			public object ColumnNames(string TableName) {
				List<string> colnames = new List<string>();
				for (int i = 0; i < DBSet.Tables[TableName].Columns.Count; i++) {
					colnames.Add(DBSet.Tables[TableName].Columns[i].ToString ());
					print (DBSet.Tables[TableName].Columns[i].ToString ());
				}
				return colnames;
			}
		}

		//////////////////////////////////////
		///// PlayerPrefs                /////
		//////////////////////////////////////
		public class UserPrefsSystem { //: Database {
			public UserPrefsSystem() {
				//check if the table userprefs exists, if not add it
				if (DBSet.Tables.Contains("UserPrefs") == false) {
					AddTable ("UserPrefs");
				}
			}
			public void Delete(string key) {
				DBSet.Tables["UserPrefs"].Columns.Remove (key);
				SaveDatabase ();
			}
			public object this[string key] {
				get { return RtData(key); }
				set	{ StData(key, value); }
			}
			private object RtData(string key) { //returns info about the userpref object.
				if (DBSet.Tables["UserPrefs"].Columns.Contains(key) == false) { return false; } // col doesnt even exist.
				else {
					if (DBSet.Tables["UserPrefs"].Rows.Count == 0) { return false; } // the colname exists but no data under it.
					else {
						string lastrow = DBSet.Tables["UserPrefs"].Rows[DBSet.Tables["UserPrefs"].Rows.Count-1][key].ToString ();
						return lastrow;
					}
				}
			}
			private void StData(string key, object value) {
				//check if the column we want exists. 
				if (DBSet.Tables["UserPrefs"].Columns.Contains(key) == false) {
					AddColTo("UserPrefs", key, value.GetType());
				}
				
				// check if any rows exist in the UserPrefs. Add the value as a new row to the pertaining column.
				if (DBSet.Tables["UserPrefs"].Rows.Count == 0) { 
					Hashtable hsh = new Hashtable();
					hsh.Add (key, value);
					AddRowTo ("UserPrefs", hsh);
				}
				else { // If it has rows just edit the spot.
					DBSet.Tables["UserPrefs"].Rows[0][key] = value;
					SaveDatabase ();
				}
			}
		}
	}



	// Use this for initialization
	void Start () {


	}
}
