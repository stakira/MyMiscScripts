{
	// ============================================================================
	// File:	Lrc2AE.jsx
	// Version:	1.0
	// Author:	Sugita Akira
	// Date:	04/08/2013
	// Description:
	//		This script import a lrc file into After Effects, creating a text layer
	//		for each lrc line, and place the layer in composition timeline
	//		according to lrc time tags.
	// ============================================================================

	// ============================================================================
	// Function: is_empty_line
	// ============================================================================
	function is_empty_line(lrc_line) {
		var patt_empty = /^\s*$/;
		return patt_empty.test(lrc_line)
	}

	// ============================================================================
	// Function: extract_text
	// ============================================================================
	function extract_text(lrc_line) {
		var patt_tag = /\[[0-9.:]+\]/g;
		var text_line = lrc_line.replace(patt_tag, "");
		return(text_line);
	}

	// ============================================================================
	// Function: extract_time
	// ============================================================================
	function extract_time(lrc_line) {
		var patt = /[0-9]+/g;
		var result = lrc_line.match(patt);
		var time = parseFloat(result[0]) * 60
				 + parseFloat(result[1])
				 + parseFloat(result[2])/100;
		return time;
	}

	// ============================================================================
	// Main Script
	// ============================================================================
	app.beginUndoGroup("Load a lrc file");

	// prepare layers
	var actiItem = app.project.activeItem;
	if(actiItem == null || !(actiItem instanceof CompItem)) {
		actiItem = app.project.items.addComp('Lrc2AE',1280,720,1,10,25);
		alert("New Comp created");
	}
	var lrc_layers = actiItem.layers;

	// Open lrc file
	var lrc_file = File.openDialog("select lrc file","*lrc");
	var lrc_line = "";
	var text_obj = lrc_layers.addNull();
	text_obj.name = "Imported with Lrc2AE";

	if(lrc_file != null) {
		lrc_file.open("r","TEXT","????");
		while(!(lrc_file.eof)) {
			// read next line
			lrc_line = lrc_file.readln();

			// line operation
			if (!is_empty_line(lrc_line)) {
				text_obj.outPoint = extract_time(lrc_line);		// outPoint of last layer
				text_obj = lrc_layers.addText(extract_text(lrc_line));
				text_obj.startTime = 0;
				text_obj.inPoint = extract_time(lrc_line);		// inPoint of current layer
			}
		}
	}
	text_obj.outPoint = text_obj.outPoint - extract_time(lrc_line);
	alert("Completed!\n\nLrc2AE\nv1.0\nBy Sugita Akira\nhttp://weibo.com/sugitaakira");

	app.endUndoGroup();
}
