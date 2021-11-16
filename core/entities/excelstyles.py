# -*- encoding:UTF-8 -*-
'''
Created on 2020/5/3

@author: xcKev
'''

from openpyxl.styles import Font, PatternFill, Protection, Alignment, Border, Side, NamedStyle, colors

class ExcelFont(object):
    
    def __init__(self, _name='Times New Roman', _size=12, _bold=False, _strike=False, _italic=False, _color=colors.BLACK):
        self._font = Font()
        self._font.name = _name
        self._font.size = _size
        self._font.bold = _bold
        self._font.strike = _strike
        self._font.italic = _italic
        self._font.color = _color
        
    def get_font(self):
        return self._font
    
class ExcelBorders(object):
    
    def __init__(self, _left_side, _right_side, _top_side, _bottom_side):
        self._border = Border(left=Side(border_style='thin', color='000000'), right=Side(border_style='thin', color='000000'), top=Side(border_style='thin', color='000000'), bottom=Side(border_style='thin', color='000000'))  # Create Borders
        # 'dashDot','dashDotDot','dashed','dotted','double','hair','medium','mediumDashDot','mediumDashDotDot','mediumDashed','slantDashDot','thick','thin'
        if _left_side:
            self._border.left = _left_side
        if _right_side:
            self._border.right = _right_side
        if _top_side:
            self._border.top = _top_side
        if _bottom_side:
            self._border.bottom = _bottom_side
        
    def get_border(self):
        return self._border
    
class ExcelPattern(object):
    def __init__(self, fill_type=None, start_color='FFFFFF', end_color='000000'):
        self.pattern = PatternFill(fill_type=fill_type, start_color=start_color, end_color=end_color)
        # fill_type# 'none'、'solid'、'darkDown'、'darkGray'、'darkGrid'、'darkHorizontal'、'darkTrellis'、'darkUp'、'darkVertical'、'gray0625'、'gray125'、'lightDown'、'lightGray'、'lightGrid'、'lightHorizontal'、'lightTrellis'、'lightUp'、'lightVertical'、'mediumGray'
        
    def get_pattern(self):
        return self.pattern
    
class ExcelAlignment(object):
    def __init__(self, _horz='left', _vert='center', _wrap_text=True):
        self.alignment = Alignment()
        self.alignment.horizontal = _horz  # left,right,center,distributed,centerContinuous,justify,fill,general
        self.alignment.vertical = _vert  # center,top,bottom,justify,distributed
        self.alignment.wrap_text = _wrap_text
        
    def get_alignment(self):
        return self.alignment

class ExcelProtection(object):
    
    def __init__(self, _locked=False, _hidden=False):
        self._protection = Protection(locked=_locked, hidden=_hidden)
    
    def get_protection(self):
        return self._protection
    
class ExcelStyle(object):
    
    def __init__(self, font=None, border=None, protection=None, alignment=None, pattern_fill=None):
        self._style = NamedStyle()
        if font:
            self._style.font = font.get_font()
        if border:
            self._style.border = border.get_border()
        if protection:
            self._style.protection = protection.get_protection()
        if alignment:
            self._style.alignment = alignment.get_alignment()
        if pattern_fill:
            self._style.fill = pattern_fill.get_pattern()
    
    def get_style(self):
        return self._style
