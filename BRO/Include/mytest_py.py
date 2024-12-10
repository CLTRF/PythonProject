#import report
#import mpld3


html=""
w = lambda s: s + "\n"

def generate_hr(width="100%", color="black", height="2px", margin="20px auto"):
    hr_html = f'<hr style="width: {width}; margin: {margin}; border: none; height: {height}; background-color: {color};">'
    return hr_html


html +=w(report.html_header())  
html +=w("<p>" + report.png_to_html(filename="./img/gomspace_logo_dark.png", width=300) + "</p>") 
html += w("<h1>VHF payload,FM satellite,Hot TVAC test </h1>") 
html += w("\n<br />")
html += w("\n<br />")
html += w("<h2>Checkout information</h2>")
html += report.dataframe_to_html(info_checkout,index=False)  
html += w("\n<br />")
html += w("<h2>Instrument Information</h2>")
html += w("The checkout has been conducted using the instruments listed below unless otherwise noted.\n<br />")
html += report.dataframe_to_html(info_instrument,index=False)  
html += w("\n<br />")
html += w("\n<br />")



html += w("<h2>SW information</h2>")
#SW information table
html += report.dataframe_to_html(myinfo1,index=False)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
#Vfem id

html += w("<h2>VFEM module Information</h2>")
html += report.dataframe_to_html(myinfo2)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
##############TX voice mode#################################### 
#Power measured
#Power estimated 
#Thd
#AM index
#PA Temperature
#Vbat
#Ibat
html += w("<h2>VHF payload TX voice </h2>")
html +=generate_hr(width="50%", color="black", height="3px", margin="20px 0 20px 0")
html += w("\n<br />")
html += w("\n<br />")
html += w("<h3>Test setup</h3>")
html += w("The satellite is supply by an external 32V power supply \n<br />")
html +=w("<p>" + report.png_to_html(filename="./img/TX_testsetup.png", width=600) + "</p>") 
html += w("<h3>Power measured</h3>")
html += report.dataframe_to_html(Power_tx_voice)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
html += w("<h3>Power estimated</h3>")
#html += report.dataframe_to_html(Pest_tx_voice)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
html +=w("<p>" + report.png_to_html(filename='./img_data/TX_voice_power.png', width=600) + "</p>") 
html += w("<h3>THD</h3>")
html += report.dataframe_to_html(Thd_tx_voice)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
html += w("<h3>AM index</h3>")
html += report.dataframe_to_html(AMindex_tx_voice)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
html += w("<h3>PA Temperature</h3>")
html +=w("<p>" + report.png_to_html(filename='./img_data/TX_voice_temp.png', width=600) + "</p>") 
#html += report.dataframe_to_html(p_style)   #insert correct table
html += w("\n<br />")
html += w("\n<br />")
html += w("<h3>Voltage Vfem</h3>")
html += report.dataframe_to_html(Voltage_tx_voice)   #insert correct table
html += w("<h3>Current Vfem</h3>")
html += report.dataframe_to_html(Current_tx_voice)
html +=w("<p>" + report.png_to_html(filename="./img_data/TX_voice_voltage.png", width=600) + "</p>") 


CHECKOUT_FORM_CONFORMITY = 'It is hereby certified that apart from the deviations or waivers noted in the "Remarks" box below, the whole of the item detailed above, conform in all respects to the specification(s),\n<br /> drawing(s) and condition(s) or requirement(s) respects to the specification(s), drawing(s) and condition(s) or requirement(s) of the contract.'

html += w("<h2>Statement of conformity</h2>")
html += w("<p>" + CHECKOUT_FORM_CONFORMITY + "</p>")
html += w("<p><b>Remarks:</b><br /><table><tr><td> NOT correct software, need to update power estimated and RX data.   \n<br /> \n<br />\n<br />\n<br />\n<br />\n<br />\n<br />\n<br /></td></tr></table></p>")
html += w("<h2>Document information</h2>")
#html += w("<p>" + html + "</p>")
html += w(report.html_page_break())






html +=w(report.html_footer())
output = "FM_payload.html"

with open(output, "w") as fh:
        fh.write(html)
    

