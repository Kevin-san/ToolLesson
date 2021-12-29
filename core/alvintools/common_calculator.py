#-*-coding:utf-8-*-
'''
Created on 2021/2/13

@author: xcKev
'''
import PdfWeb.db as db
from alvintools import common_tools
temperature_units={"摄氏度":"c","华氏度":"f","开氏度":"k","兰氏度":"r","列氏度":"l"}
unit_key_vals_dict={
    'angle':{
    '圆周':['度',360],
    '弧度':['度',57.2958],
    '毫弧度':['度',0.0572958],
    '度':['度',1],
    '直角':['度',90],
    '百分度':['度',0.01],
    '秒':['度',3600],
    '分':['度',60]
    },
    'time':{
    '年':['秒',31536000],
    '周':['秒',604800],
    '天':['秒',86400],
    '时':['秒',3600],
    '分':['秒',60],
    '秒':['秒',1],
    '毫秒':['秒',0.01]
    },
    'heat':{
    '卡':['卡',1],
    '千卡':['卡',1000],
    '千瓦·时':['卡',860040],
    '英制马力·时':['卡',641331.7179],
    '米制马力·时':['卡',632558.3449],
    '公斤·米':['卡',2.3421],
    '英热单位':['卡',252.05],
    '英尺·磅':['卡',0.3239]
    },
    'length':{
    '公里':['纳米',1000000000000],
    '米':['纳米',1000000000],
    '分米':['纳米',100000000],
    '厘米':['纳米',10000000],
    '毫米':['纳米',1000000],
    '丝':['纳米',100000],
    '微米':['纳米',1000],
    '里':['纳米',500000000000],
    '丈':['纳米',3333333333.3333],
    '尺':['纳米',333333333.3333],
    '寸':['纳米',33333333.3333],
    '分':['纳米',3333333.3333],
    '厘':['纳米',333333.3333],
    '海里':['纳米',1852000000000],
    '英寻':['纳米',1828800000],
    '英里':['纳米',1609344000000],
    '弗隆':['纳米',201168000000],
    '码':['纳米',914400000],
    '英尺':['纳米',304800000],
    '英寸':['纳米',25400000],
    '纳米':['纳米',1],
    '皮米':['纳米',0.001],
    '光年':['纳米',9460700000000000000000000],
    '天文单位':['纳米',149600000000000000000]
    },
    'area':{
    '平方千米':['平方毫米',1000000000000],
    '公顷':['平方毫米',10000000000],
    '公亩':['平方毫米',100000000],
    '平方米':['平方毫米',1000000],
    '平方分米':['平方毫米',10000],
    '平方厘米':['平方毫米',100],
    '平方毫米':['平方毫米',1],
    '英亩':['平方毫米',4046856422.4],
    '平方英里':['平方毫米',2589988110336],
    '平方码':['平方毫米',836127.36],
    '平方英尺':['平方毫米',92903.04],
    '平方英寸':['平方毫米',645.16],
    '平方竿':['平方毫米',25292852.64],
    '顷':['平方毫米',66666666666.67],
    '亩':['平方毫米',666666666.6667],
    '分':['平方毫米',66666666.66667],
    '平方尺':['平方毫米',111111.1111],
    '平方寸':['平方毫米',1111.1111]
    },
    'speed':{
    '米/秒':['千米/时',3.6],
    '千米/秒':['千米/时',3600],
    '千米/时':['千米/时',1],
    '英寸/秒':['千米/时',0.09144],
    '英里/时':['千米/时',1.609344],
    '马赫':['千米/时',1225.08],
    '光速':['千米/时',1079252848.8]
    },
    'byte':{
    '比特':['比特',1],
    '字节':['比特',8],
    '千字节':['比特',8192],
    '兆字节':['比特',8388608],
    '千兆字节':['比特',8589934592],
    '太字节':['比特',8796093022208],
    '拍字节':['比特',9007199254740992],
    '艾字节':['比特',9223372036854775808]
    },
    'power':{
    '瓦':['瓦',1],
    '千瓦':['瓦',1000],
    '英制马力':['瓦',745.6998],
    '米制马力':['瓦',735.4987],
    '公斤·米/秒':['瓦',9.8066],
    '千卡/秒':['瓦',4184.1004],
    '英热单位/秒':['瓦',1055.0559],
    '英尺·磅/秒':['瓦',1.3558],
    '焦耳/秒':['瓦',1],
    '牛顿·米/秒':['瓦',1]
    },
    'pressure':{
    '帕斯卡':['帕斯卡',1],
    '兆帕':['帕斯卡',1000000],
    '千帕':['帕斯卡',1000],
    '百帕':['帕斯卡',100],
    '标准大气压':['帕斯卡',101325],
    '毫米汞柱':['帕斯卡',133.3224],
    '英寸汞柱':['帕斯卡',3386.3881],
    '巴':['帕斯卡',100000],
    '毫巴':['帕斯卡',100],
    '磅力/平方英尺':['帕斯卡',47.8802],
    '磅力/平方英寸':['帕斯卡',6894.757],
    '毫米水柱':['帕斯卡',9.8066],
    '公斤力/平方厘米':['帕斯卡',98066.5],
    '公斤力/平方米':['帕斯卡',9.80665]
    },
    'density':{
    '克/立方厘米':['克/立方厘米',1],
    '克/立方分米':['克/立方厘米',0.001],
    '克/立方米':['克/立方厘米',0.000001],
    '千克/立方厘米':['克/立方厘米',1000],
    '千克/立方分米':['克/立方厘米',1],
    '千克/立方米':['克/立方厘米',0.001]
    },
    'force':{
    '牛':['牛',1],
    '千牛':['牛',1000],
    '千克力':['牛',9.80665],
    '克力':['牛',0.0098067],
    '公吨力':['牛',9806.65],
    '磅力':['牛',4.4482],
    '千磅力':['牛',4448.2216],
    '达因':['牛',0.00001]
    },
    'volume':{
    '立方毫米':['立方毫米',1],
    '立方厘米':['立方毫米',1000], 
    '立方分米':['立方毫米',1000000],
    '立方米':['立方毫米',1000000000],
    '立方千米':['立方毫米',1000000000000000000],
    '升':['立方毫米',1000000],
    '分升':['立方毫米',100000],
    '毫升':['立方毫米',1000],
    '厘升':['立方毫米',10000],
    '公石':['立方毫米',100000000],
    '微升':['立方毫米',1],
    '立方英尺':['立方毫米',28316800],
    '立方英寸':['立方毫米',16387.0370],
    '立方码':['立方毫米',764553600],
    '亩英尺':['立方毫米',1233481837548],
    '英制加仑':['立方毫米',4546091.88],
    '美制加仑':['立方毫米',3785411.784],
    '英制液体盎司':['立方毫米',28410],
    '美制液体盎司':['立方毫米',29570]
    },
    'quality':{
    '千克':['微克',1000000000],
    '克':['微克',1000000],
    '毫克':['微克',1000],
    '微克':['微克',1],
    '吨':['微克',1000000000000],
    '公担':['微克',100000000000],
    '克拉':['微克',200000],
    '分':['微克',2000],
    '磅':['微克',453592370],
    '盎司':['微克',28349523.125],
    '格令':['微克',64798.91],
    '长吨':['微克',1016046908800],
    '短吨':['微克',907184740000],
    '英担':['微克',50802345440],
    '美担':['微克',45359237000],
    '英石':['微克',6350293180],
    '打兰':['微克',1771845.1953],
    '担':['微克',50000000000],
    '斤':['微克',500000000],
    '两':['微克',50000000],
    '钱':['微克',5000000]
    }
}
def calculator_by_type(conversion_type,calc_str):
    unit_key_vals={}
    try:
        unit_dict_list=db.get_unit_dictionary_by_conversion_type(conversion_type)
        for unit_dict in unit_dict_list:
            unit_key_vals[unit_dict.UnitFromKey]=[unit_dict.UnitToKey,unit_dict.UnitValue]
    except:
        unit_key_vals=unit_key_vals_dict[conversion_type]
    for key in unit_key_vals.keys():
        check_val = calc_str.split(key)[0]
        if common_tools.is_number(check_val):
            to_val = unit_key_vals[key][1]*float(check_val)
            return unitsoutput(unit_key_vals,to_val)
    return invalid_output(unit_key_vals)

def unitsoutput(unit_key_vals,to_val):
    unit_output=[]
    for unit,val_list in unit_key_vals.items():
        convert_val=to_val/val_list[1]
        unit_output.append(F"{convert_val}{unit}")
    return "\n".join(unit_output)

def invalid_output(unit_key_vals):
    outputs=[]
    for output_val in unit_key_vals.keys():
        outputs.append(output_val)
    output_str="||".join(outputs)
    return F"invalid input,pls input like this: 1{output_str}"

def calc_angle(calc_str):
    return calculator_by_type("angle",calc_str)

def calc_time(calc_str):
    return calculator_by_type("time",calc_str)

def calc_heat(calc_str):
    return calculator_by_type("heat",calc_str)

def calc_length(calc_str):
    return calculator_by_type("length",calc_str)

def calc_area(calc_str):
    return calculator_by_type("area",calc_str)

def calc_speed(calc_str):
    return calculator_by_type("speed",calc_str)

def calc_byte(calc_str):
    return calculator_by_type("byte",calc_str)

def calc_power(calc_str):
    return calculator_by_type("power",calc_str)

def calc_pressure(calc_str):
    return calculator_by_type("pressure",calc_str)

def calc_density(calc_str):
    return calculator_by_type("density",calc_str)

def calc_force(calc_str):
    return calculator_by_type("force",calc_str)

def calc_volume(calc_str):
    return calculator_by_type("volume",calc_str)

def calc_quality(calc_str):
    return calculator_by_type("quality",calc_str)

def calc_temperature(calc_str):
    for key in temperature_units.keys():
        if key in calc_str:
            c_val=unit2c(key,float(calc_str.split(key)[0]))
            return c2outputs(c_val)
    return "invalid input,pls input like this: 1摄氏度/华氏度/开氏度/兰氏度/列氏度"

def unit2c(unit,calc_val):
    from_unit=temperature_units[unit]
    method=F"{from_unit}2c"
    return eval(method)(calc_val)

def c2outputs(calc_val):
    outputs=[]
    for key,val in temperature_units.items():
        convert_method=F"c2{val}"
        output_val=eval(convert_method)(calc_val)
        outputs.append(F"{output_val}{key}")
    return "\n".join(outputs)
        
def c2c(calc_val):
    return calc_val

def f2c(calc_val):
    return (calc_val-32)/1.8

def c2f(calc_val):
    return 32+calc_val*1.8

def k2c(calc_val):
    return calc_val-273.15

def c2k(calc_val):
    return calc_val+273.15

def r2c(calc_val):
    return (calc_val*1.8)-273.15

def c2r(calc_val):
    return (calc_val+273.15)*5/9

def l2c(calc_val):
    return 1.25*calc_val

def c2l(calc_val):
    return calc_val/1.25
