## 更新翻译

1. **terminal 依次输入 (在项目根目录)**
   * 提取所有的要翻译的string

     ~~~sh
     pybabel extract -F babel.cfg -o messages.pot .
     ~~~

   * 更新translations/zh/LC_MESSAGES/目录下的翻译目录

     ~~~sh
     pybabel update -i messages.pot -d translations
     ~~~

3. 进入 translations/zh/LC_MESSAGES/messages.po 然后根据msgid补充msgstr (翻译)

   或者你可以运行该translations/目录下的translator.py，它会自动填充，但请做检查（避免%(xxx)中的xxx也被翻译）

4. 编译生成翻译文件

   ~~~sh
    pybabel compile -d translations
   ~~~

   

