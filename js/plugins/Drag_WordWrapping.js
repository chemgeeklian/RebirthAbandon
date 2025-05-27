//=============================================================================
// Drag_WordWrapping.js
//=============================================================================

/*:
 * @target MZ
 * @plugindesc A word wrapping plugin for MZ.
 * v1.10.0
 *
 * @author Drag
 *
 * @url
 *
 * @help 
 *
 * This plug and play plugin will attempt to correctly and automatically
 * place line break in your text box and ensure a correct word wrapping,
 * so you don't have to bother with all of that anymore.
 *
 * @param offset
 * @desc Increasing this value will make your text being word-wrapped closer from the left.
 * @type number
 * @text Right Offset
 * @default 15
 *
 * @param calcFaceWidth
 * @desc Weither or not face width should be taken in account when word-wrapping.
 * @type boolean
 * @text Calc Face Width
 * @default true
 *
 */

var Imported = Imported || {};
Imported.wordWrapping = true;

var Drag = Drag || {};
Drag.wordWrapping = Drag.wordWrapping || {};
Drag.wordWrapping.version = 1.10;

(function() {

	Drag.wordWrapping.pluginName = "Drag_WordWrapping";
	
	Drag.wordWrapping.params = PluginManager.parameters(Drag.wordWrapping.pluginName) || null;
	if (Drag.wordWrapping.params) {
		Drag.wordWrapping.params.offset = parseInt(Drag.wordWrapping.params.offset) || 15;
		Drag.wordWrapping.params.calcFaceWidth = Drag.wordWrapping.params.calcFaceWidth === "false" ? false : true;
	}
	
	//-----------------------------------------------------------------------------
	// Window Message 
	
	Window_Message.prototype.createTextState = function(text, x, y, width) {
		const rtl = Utils.containsArabic(text);
		const textState = {};
		textState.width = width;
		textState.x = rtl ? x + width : x;
		textState.y = y;
		textState.startX = textState.x;
		textState.startY = textState.y;
		textState.text = this.convertEscapeCharacters(text);
		textState.text = this.placeBackToLine(textState);
		textState.index = 0;
		textState.height = this.calcTextHeight(textState);
		textState.rtl = rtl;
		textState.buffer = this.createTextBuffer(rtl);
		textState.drawing = true;
		textState.outputWidth = 0;
		textState.outputHeight = 0;
		return textState;
	};
	
	Window_Message.prototype.placeBackToLine = function(textState) {
		const x = Drag.wordWrapping.params.calcFaceWidth ? this.newLineX(textState) : 0;
		const ww = this.width;
		let newText = partText = partWordText = "";
		for (let character of textState.text) {
			if (character === " ") {
				let preProcessMessageWindow = new pre_Process_Window_Message(this.preProcessMessageWindowRect());
				let textWidth = preProcessMessageWindow.getTextWidth(partWordText + " " + partText);
				if (textWidth + x > ww - Drag.wordWrapping.params.offset) {
					newText += partWordText.trim() + "\n";
					partWordText = "";
					partText += " ";
				} else {
					partWordText += " " + partText;
					partText = "";
				}
			} else {
				partText += character;
			}			
		}
		newText += (partWordText + " " + partText).trim();
		return newText.replace("  ", " ");
	};
	
	Window_Message.prototype.preProcessMessageWindowRect = function() {
		const ww = 0
		const wh = 0
		const wx = 0
		const wy = 0;
		return new Rectangle(wx, wy, ww, wh);
	};
	
	Window_Message.prototype.getMessageFaceSize = function() {
		const width = ImageManager.faceWidth;
		const height = this.innerHeight;
		return [width, height];
	};
	
	//-----------------------------------------------------------------------------
	// Pre Process Window Message 
	
	function pre_Process_Window_Message() {
		this.initialize(...arguments);
	}

	pre_Process_Window_Message.prototype = Object.create(Window_Message.prototype);
	pre_Process_Window_Message.prototype.constructor = pre_Process_Window_Message;
	
	pre_Process_Window_Message.prototype.createTextState = function(text, x, y, width) {
		const rtl = Utils.containsArabic(text);
		const textState = {};
		textState.text = this.convertEscapeCharacters(text);
		textState.index = 0;
		textState.x = rtl ? x + width : x;
		textState.y = y;
		textState.width = width;
		textState.height = this.calcTextHeight(textState);
		textState.startX = textState.x;
		textState.startY = textState.y;
		textState.rtl = rtl;
		textState.buffer = this.createTextBuffer(rtl);
		textState.drawing = true;
		textState.outputWidth = 0;
		textState.outputHeight = 0;
		return textState;
	};
	
	pre_Process_Window_Message.prototype.getTextWidth = function(text) {
		this.resetFontSettings();
		const textState = this.createTextState(text, 0, 0, 0);
		this.processAllText(textState);
		return textState.outputWidth;
	};	
	
	pre_Process_Window_Message.prototype.playCharSE = function(se){}; //avoid se being duplicated for people using official plugin PlayMsgWndCharSeMZ
	
})();