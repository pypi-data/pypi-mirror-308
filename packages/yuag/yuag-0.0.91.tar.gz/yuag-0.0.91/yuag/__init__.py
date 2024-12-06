"""
مكتبة yuag
-----------------
\n\n

دليل لدوال المكتبة\n
يمكنك الدخول على كل دالة لمعرفة تفاصيلها\n

استدعاء مكتبات:
-----------------
```
PyPDF2()
Translator()
openai()
BeautifulSoup()
requests()
time()
os()
```

دوال عامة:
-----------------
```
wait()
clear()
detect_lang()
rangeNum()
python_path()
check_lib_status()
```
\n\n

دوال للملفات:
-----------------
```
filesIn()
rename()
move()
create_folder()
copy_folder()
readFile()
saveFile()
readJSON()
saveJson()
savePDF()
copy_file()
delete_file()
delete_folder()
```
\n\n

دوال للمصفوفات:
-----------------
```
equalArr()
allIndexInArr()
inArr()
onSide()
fillArr()
removeFromArr()
RemoveDuplicates()
sumArr()
minusArr()
makeColumnArr()
convertRowToCol()
addArr()
delArr()
sliceArr()
reverseArr()
search2D()
convert2D()
rotate2DArr()
insertInArr()
convertTxt()
searchIn_decodeNum()
searchInObjArr()
```
\n\n

دوال للقواميس:
-----------------
```
equalObject()
getObjectKeys()
addToObject()
key_index()
delete_key()
insert_key()
change_key()
```
\n\n

دوال لل json:
-----------------
```
combine_json_files()
uncombine_json_file()
```
\n\n

دوال لملفات القراءة:
-----------------
```
combine_pdf_files()
pdf_to_elements()
pdf_page_to_elements()
pdf_pages_num()
images_to_pdf()
```
\n\n

دوال لملفات xlsx:
-----------------
```
xlsx_to_arr()
arr_to_xlsx()
```
\n\n

دوال لملفات docx:
-----------------
```
docx_to_text()
text_to_docx()
```
\n\n

دوال النصوص:
-----------------
```
decodeNum()
right()
left()
mid()
split()
removeSpaces()
replaceText()
```
\n\n

دوال للأرقام:
-----------------
```
makeZeroNum()
toTime()
```
\n\n

دوال التقسيم:
-----------------
```
separate_text()
separate_arr()
separate_obj()
```
\n\n

دوال الترجمة:
-----------------
```
translate_text()
translate_arr()
translate_obj()
```
\n\n

دوال فصل هيكل الصفحة:
-----------------
```
decode_html_in_text()
decode_html_in_arr()
decode_html_in_obj()
```
\n\n

دوال لوحة المفاتيح:
-----------------
```
write()
press()
unpress()
copy()
```
\n\n

دوال الفارة:
-----------------
```
getMousePosition()
getMousePositions()
click()
right_click()
move()
```
\n\n

دوال ذكاء اصطناعي:
-----------------
```
chatGPT()
```
\n\n

دوال استخراج البينات من المواقع beautiful soup:
-----------------
```
get_soup()
get_file_soup()
get_redirected_url()
innerText()
innerHTML()
delete_text_out_of_html_elements()
```
\n\n

دوال استخراج البينات من المواقع selenium:
-----------------
```
makeFirefoxDriver()
driverToSoup()
```
\n\n

دوال تحويل الملفات لروابط:
-----------------
```
imageLink_to_dataurl()
imageFile_to_dataurl()
videoFile_to_dataurl()
```
\n\n

دوال اليوتيوب:
-----------------
```
video_trans()
```
\n\n

دوال التنزيل:
-----------------
```
download_file()
```
\n\n

رسالة الإنتهاء:
-----------------
```
doneMessage()
```
"""

from .yuag import *