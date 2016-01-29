#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )


class GlobalGlyph ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )

	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return "Global Glyph"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return "y"
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawGlobalGlyph( self, Layer ):

		Glyph = Layer.parent
		Font = Glyph.parent
		thisMaster = Font.selectedFontMaster
		masters = Font.masters
		Scale = self.getScale()
		try:
			# Glyphs 2 (Python 2.7)
			activeMasterIndex = masters.index(thisMaster)
		except:
			# Glyphs 1 (Python 2.6)
			for i, k in enumerate(masters):
				if thisMaster == masters[i]:
					activeMasterIndex = i

		globalGlyph = Font.glyphForName_("_global")
		if globalGlyph is None:
			return
		thisLayer = globalGlyph.layers[activeMasterIndex]


		#draw path AND components for strokes and form:

		try:
			thisBezierPathWithComponent = thisLayer.copyDecomposedLayer().bezierPath() # for Glyphs 2.2
		except:
			thisBezierPathWithComponent = thisLayer.copyDecomposedLayer().bezierPath   # for Glyphs 2.3

		if thisBezierPathWithComponent:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 0.7, 0.2, 0.1 ).set()
			thisBezierPathWithComponent.fill()
			thisBezierPathWithComponent.setLineWidth_(1 / Scale)
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 0.7, 0.2, 1.0 ).set()
			thisBezierPathWithComponent.stroke()


		# draw path for open forms

		try:
			thisOpenBezierPath = thisLayer.openBezierPath() # for Glyphs 2.2
		except:
			thisOpenBezierPath = thisLayer.openBezierPath # for Glyphs 2.3

		if thisOpenBezierPath:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 1.0, 1.0 ).set()
			thisOpenBezierPath.setLineWidth_(1 / Scale)
			thisOpenBezierPath.stroke()

	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			self.drawGlobalGlyph( Layer )
		except:
			import traceback
			print traceback.format_exc()

	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths,
		but for inactive glyphs in the Edit view.
		"""
		try:
			self.drawGlobalGlyph( Layer )
		except Exception as e:
			import traceback
			print traceback.format_exc()




	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Return False to disable the black outline. Otherwise remove the method.
		"""
		return False
	
	def getScale( self ):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
