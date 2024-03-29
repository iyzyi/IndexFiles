import sqlite3, os, re, hashlib, datetime, time

def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()

def format_path(path):
    path = path.replace('/', '\\')
    if path[-1] == '\\' and len(path) > 3:
        path = path[:-1]
    return path

def merge_path(path1, path2):
    if path1[-1] == '\\':
        return path1 + path2
    else:
        return path1 + '\\' + path2

def get_current_time_stamp():
    return int(datetime.datetime.now().timestamp())

def path_filter(path):
    path_regex = [r'^[a-zA-Z]:\\System Volume Information$', r'^[a-zA-Z]:\\\$RECYCLE\.BIN$']
    for regex in path_regex:
        res = re.search(regex, path)
        if res:
            return True
    return False


# 删除一个文件只会更新其父文件夹的修改时间，不会更改祖先文件夹的修改时间，
# 因而需要通过此函数，递归更新所有祖先文件夹的修改时间。
def update_folder_modify_time(path):
    if path_filter(path):
        return

    try:
        files = os.listdir(path)
    except PermissionError:
        return
    else:
        max_mtime = 0
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                update_folder_modify_time(file_path)
            
                mtime = os.path.getmtime(file_path)
                if mtime > max_mtime:
                    max_mtime = mtime
        
        res = re.search(r'^[a-zA-Z]:\\$', path)
        if res:
            return
        
        self_mtime = os.path.getmtime(path)
        if self_mtime > max_mtime:
            max_mtime = self_mtime
        os.utime(path, (time.time(), max_mtime))

        
        # if self_mtime != max_mtime:
        #     print('{} -> {} \t | {}'.format(self_mtime, max_mtime, path))


class MySqlite:

    def __init__(self, db_path = 'FileIndexInfo.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        self.conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)

        self.intro_vol_table_name = 'intro_vols'
        if not self.exists_table(self.intro_vol_table_name):
            self.create_intro_vols_table()
        
        self.settings_table_name = 'settings'
        if not self.exists_table(self.settings_table_name):
            self.create_settings_table()


    def root_path_to_vol_table_name(self, root_path):
        root_path = format_path(root_path)
        res = re.search(r'^([a-zA-Z]):\\?', root_path)
        if res:
            driver_letter = res.group(1).lower()
            vol_table_name = 'vol_{}_{}'.format(driver_letter, get_md5(root_path.lower()))
            return vol_table_name
        else:
            return None


    def exists_table(self, table_name):
        sql = "SELECT tbl_name FROM sqlite_master WHERE type = 'table';"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        tables = [v[0] for v in values]
        return table_name in tables


    def delete_table(self, table_name):
        print('[INFO] 删除数据库 {}'.format(table_name))
        sql = "DROP TABLE {}".format(table_name)
        self.cur.execute(sql)
        self.conn.commit()


    def create_vol_table(self, vol_table_name):
        print('[INFO] 创建数据库 {}'.format(vol_table_name))
        sql = '''CREATE TABLE {}
                    (id         INTEGER     PRIMARY KEY     AUTOINCREMENT,
                    pid         INTEGER,
                    name        VARCHAR,
                    type        CHAR(1),
                    mtime       INTEGER );'''.format(vol_table_name)
        self.cur.execute(sql)
        self.conn.commit()


    def insert_into_vol_table(self, vol_table_name, pid, name, type, mtime):
        self.cur.execute('INSERT INTO {} VALUES(NULL,?,?,?,?)'.format(vol_table_name), (pid, name, type, mtime))
        self.conn.commit()
        return self.cur.lastrowid


    def insert_root_path_into_vol_table(self, vol_table_name, root_path):
        root_path_id = self.insert_into_vol_table(vol_table_name, 0, root_path, 'R', 0)
        return root_path_id


    def get_id_and_name_and_type_and_mtime(self, vol_table_name, pid):
        sql = "SELECT id, name, type, mtime FROM {} WHERE pid={};".format(vol_table_name, pid)
        self.cur.execute(sql)
        values = self.cur.fetchall()
        return values
    

    def get_sub_id_and_type(self, vol_table_name, pid):
        sql = "SELECT id, type FROM {} WHERE pid={};".format(vol_table_name, pid)
        self.cur.execute(sql)
        values = self.cur.fetchall()
        return values
    

    def delete_item_by_id(self, table_name, id):
        sql = "DELETE FROM {} WHERE id={}".format(table_name, id)
        #print(sql)
        self.cur.execute(sql)
        self.conn.commit()
        

    def delete_item_by_pid(self, table_name, pid):
        sql = "DELETE FROM {} WHERE pid={}".format(table_name, pid)
        #print(sql)
        self.cur.execute(sql)
        self.conn.commit()


    def get_root_path_id(self, vol_table_name, root_path):
        sql = "SELECT id FROM {} WHERE name='{}';".format(vol_table_name, root_path.replace("'", "''"))
        self.cur.execute(sql)
        values = self.cur.fetchall()
        return None if values == [] else values[0][0]


    def get_id_and_mtime(self, table_name, pid, name):
        sql = "SELECT id, mtime FROM {} WHERE pid={} and name='{}';".format(table_name, pid, name.replace("'", "''"))
        self.cur.execute(sql)
        values = self.cur.fetchall()
        return None if values == [] else values[0]
    
    def update_mtime_vol_table(self, vol_table_name, id, mtime):
        sql = "UPDATE {} SET mtime={} WHERE id={};".format(vol_table_name, mtime, id)
        self.cur.execute(sql)
        self.conn.commit()


    def create_intro_vols_table(self):
        print('[INFO] 创建数据库 {}'.format(self.intro_vol_table_name))
        sql = '''CREATE TABLE {}
                    (vol_id         INTEGER     PRIMARY KEY     AUTOINCREMENT,
                    vol_name        VARCHAR,
                    vol_path        VARCHAR,
                    dirs_num        INTEGER,
                    files_num       INTEGER,
                    update_time     INTEGER,
                    working         CHAR(1) );'''.format(self.intro_vol_table_name)
        self.cur.execute(sql)
        self.conn.commit()


    def insert_into_intro_vols_table(self, vol_table_name, root_path):
        sql = "INSERT INTO {} VALUES(NULL,?,?,?,?,?,?)".format(self.intro_vol_table_name)
        self.cur.execute(sql, (vol_table_name, root_path, 0, 0, 0, 'T'))
        self.conn.commit()


    def update_intro_vols_table(self, vol_table_name, dirs_num, files_num, update_time):
        sql = "UPDATE {} SET dirs_num={}, files_num={}, update_time={}, working='{}' WHERE vol_name='{}';".format(self.intro_vol_table_name, dirs_num, files_num, update_time, 'F', vol_table_name)
        self.cur.execute(sql)
        self.conn.commit()
    

    def create_settings_table(self):
        print('[INFO] 创建数据库 {}'.format(self.settings_table_name))
        sql = '''CREATE TABLE {}
                    (id     INTEGER     PRIMARY KEY     AUTOINCREMENT,
                    key     VARCHAR,
                    value   VARCHAR);'''.format(self.settings_table_name)
        self.cur.execute(sql)
        self.conn.commit()
    
    
    def select_from_settings_table(self, key):
        sql = "SELECT value FROM {} WHERE key='{}'".format(self.settings_table_name, key)
        self.cur.execute(sql)
        return self.cur.fetchone()


    def insert_into_settings_table(self, key, value):
        sql = "INSERT INTO {} VALUES(NULL,?,?)".format(self.settings_table_name)
        self.cur.execute(sql, (key, value))
        self.conn.commit()


    def update_settings_table(self, key, value):
        sql = "UPDATE {} SET value='{}' WHERE key='{}';".format(self.settings_table_name, value, key)
        self.cur.execute(sql)
        self.conn.commit()


    # 删除此项及其全部子项的记录
    def delete_items(self, table_name, id, type='', root=True):
        items = self.get_sub_id_and_type(table_name, id)
        for sub_id, sub_type in items:
            if sub_type != 'F':
                self.delete_items(table_name, sub_id, sub_type, False)
        if type != 'F':
            self.delete_item_by_pid(table_name, id)
        if root == True:
            self.delete_item_by_id(table_name, id)
    

    def list_files(self, path, pid, table_name):
        if path_filter(path):
            return
    
        try:
            files = os.listdir(path)
        except PermissionError:
            return
        else:

            # 从数据库中删除 数据库中含有 而 本地硬盘中不含有 的文件(夹) 的记录
            db_data = self.get_id_and_name_and_type_and_mtime(table_name, pid)
            db_files_dict = {}
            if db_data:
                for id, name, type, mtime in db_data:
                    key = type + name
                    db_files_dict[key] = (id, mtime)
                
                    if name not in files:
                        self.delete_items(table_name, id)
                    else:
                        file_path = os.path.join(path, name)
                        if (type == 'F' and os.path.isdir(file_path)) or (type == 'D' and os.path.isfile(file_path)):
                            self.delete_items(table_name, id)

            def get_file_info(type, file_name):
                key = type + file_name
                return db_files_dict[key] if key in db_files_dict else None

            # 开始list
            for file in files:
                file_path = os.path.join(path, file)
                mtime_disk = int(os.path.getmtime(file_path))
                # res = self.get_id_and_mtime(table_name, pid, file)

                type = 'F' if os.path.isfile(file_path) else 'D'
                res = get_file_info(type, file)
                
                # 数据库中无此项，直接插入
                if res == None:
                    if os.path.isdir(file_path):                             
                        id = self.insert_into_vol_table(table_name, pid, file, 'D', mtime_disk)
                        self.list_files(file_path, id, table_name)
                    else:
                        id = self.insert_into_vol_table(table_name, pid, file, 'F', mtime_disk)

                # 数据库中有此项，判断修改时间是否相同，相同则跳过，不同则更新。
                else:
                    id, mtime_database = res[0], res[1]
                    if type == 'D':
                        if mtime_disk != mtime_database:
                            self.update_mtime_vol_table(table_name, id, mtime_disk)
                            self.list_files(file_path, id, table_name)
                    else:
                        if mtime_disk != mtime_database:
                            self.update_mtime_vol_table(table_name, id, mtime_disk)


    def final_summary(self, root_path, vol_table_name):
        sql = "SELECT COUNT(*) FROM {} WHERE type='D' or type='R'".format(vol_table_name)
        self.cur.execute(sql)
        dirs_num = self.cur.fetchone()[0]
        
        sql = "SELECT COUNT(*) FROM {} WHERE type='F'".format(vol_table_name)
        self.cur.execute(sql)
        files_num = self.cur.fetchone()[0]

        print('[INFO] 目录{} 中共有{}个文件夹，{}个文件'.format(root_path, dirs_num, files_num))
        update_time = get_current_time_stamp()
        self.update_intro_vols_table(vol_table_name, dirs_num, files_num, update_time)

        return dirs_num, files_num


    def get_parent(self, table_name, pid):
        sql = 'SELECT id, pid, name, type FROM {} WHERE id={}'.format(table_name, pid)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        id, pid, name, type = res
        if type == 'R':
            return name
        else:
            return merge_path(self.get_parent(table_name, pid), name)


#################################### 接口函数 ####################################

    # 建立文件索引
    def BuildFilesIndex(self, root_path):
        root_path = format_path(root_path)
        vol_table_name = self.root_path_to_vol_table_name(root_path)
        if vol_table_name == None:
            print('[ERROR] {} 不满足有效路径格式'.format(root_path))
            return
        if not os.path.exists(root_path) or not os.path.isdir(root_path):
            print('[ERROR] {} 不存在或非有效目录'.format(root_path))
            return
        
        # 删除一个文件只会更新其父文件夹的修改时间，不会更改祖先文件夹的修改时间，
        # 因而需要通过此函数，递归更新所有祖先文件夹的修改时间。
        print('[INFO] 正在更新{} 目录下的所有文件夹的修改时间'.format(root_path))
        update_folder_modify_time(root_path)
        
        # 如果以前索引过此路径，且未索引完，则删除相关索引数据
        sql = "SELECT vol_path FROM {} WHERE working='T' and vol_name='{}'".format(self.intro_vol_table_name, vol_table_name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for item in res:
            root_path = item[0]
            self.DeleteFilesIndex(root_path)

        # # 如果以前索引过此路径，则直接删除以前的相关索引数据
        # if self.exists_table(vol_table_name):
        #     self.DeleteFilesIndex(root_path)

        if not self.exists_table(vol_table_name):
            # 将本vol的相关信息写入intro_vol_table表中
            self.insert_into_intro_vols_table(vol_table_name, root_path)

            # 创建表
            vol_table_name = self.root_path_to_vol_table_name(root_path)
            self.create_vol_table(vol_table_name)

        # 插入根目录
        root_path_id = self.get_root_path_id(vol_table_name, root_path)
        if not root_path_id:
            root_path_id = self.insert_root_path_into_vol_table(vol_table_name, root_path)
        
        print('[INFO] 正在{} 目录下进行文件索引'.format(root_path))
        self.list_files(root_path, root_path_id, vol_table_name)

        # 更新intro_vol_table表中的本vol的相关信息
        return self.final_summary(root_path, vol_table_name)


    # 进行文件检索
    def SearchFiles(self, root_path, filter='', filter_mode='common'):
        root_path = format_path(root_path)
        vol_table_name = self.root_path_to_vol_table_name(root_path)
        if vol_table_name == None:
            print('[ERROR] {} 不满足有效路径格式'.format(root_path))
            return

        sql = "SELECT * FROM {} WHERE vol_name='{}'".format(self.intro_vol_table_name, vol_table_name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        if res == []:
            print('[ERROR] 目录{} 尚未被索引'.format(root_path))
            return

        if filter == '':
            sql = "SELECT id, pid, name, type FROM {}".format(vol_table_name)
        elif filter_mode == 'common':
            sql = "SELECT id, pid, name, type FROM {} WHERE name LIKE '%{}%'".format(vol_table_name, filter)
        elif filter_mode == 'regexp':
            sql = "SELECT id, pid, name, type FROM {} WHERE name REGEXP '{}'".format(vol_table_name, filter)
        else:
            print('[ERROR] filter_mode仅可选择common或regexp')
            return
        
        result = []
        files_num = 0
        dirs_num = 0
        self.cur.execute(sql)
        for one in self.cur.fetchall():
            id, pid, name, type = one

            if type == 'F' or type == 'D':
                parent_path = self.get_parent(vol_table_name, pid)
                file_path = merge_path(parent_path, name)
            elif type == 'R':
                file_path = name

            if type == 'F':
                files_num += 1
            elif type == 'D' or type == 'R':
                dirs_num += 1

            result.append((file_path, type))

        print('[FILTER: {}] {} 目录下共检索到{}个文件夹，{}个文件'.format(filter, root_path, dirs_num, files_num))
        # for item in result:
        #     file_path, type = item
        #     print('{}\t{}'.format(type, file_path))
        return result, dirs_num, files_num


    # 在多vol中进行文件检索
    def MultiVolSearchFiles(self, root_path_list, filter='', filter_mode='common'):
        result = []
        dirs_num = 0
        files_num = 0
        for root_path in root_path_list:
            res = self.SearchFiles(root_path, filter, filter_mode)
            if res != None:
                result += res[0]
                dirs_num += res[1]
                files_num += res[2]
        return result, dirs_num, files_num


    # 删除文件索引
    def DeleteFilesIndex(self, root_path):
        root_path = format_path(root_path)
        vol_table_name = self.root_path_to_vol_table_name(root_path)
        if vol_table_name == None:
            print('[ERROR] {} 不满足有效路径格式'.format(root_path))
            return

        # 删除vol_table表
        if self.exists_table(vol_table_name):
            self.delete_table(vol_table_name)
        
        # 删除 intro_vol_table表中的关于vol_table的记录行
        sql = "DELETE FROM {} WHERE vol_name='{}'".format(self.intro_vol_table_name, vol_table_name)
        self.cur.execute(sql)
        self.conn.commit()


    # 清理无效数据
    def CleanInvalidData(self):
        sql = "SELECT vol_path FROM {} WHERE working='T'".format(self.intro_vol_table_name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for item in res:
            root_path = item[0]
            self.DeleteFilesIndex(root_path)


    # 展示已索引目录
    def DisplayPaths(self):
        sql = "SELECT * FROM {}".format(self.intro_vol_table_name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        # for item in res:
        #     vol_id, vol_name, vol_path, dirs_num, files_num, writing = item
        #     print(vol_id, vol_name, vol_path, dirs_num, files_num, writing)
        sorted_res = sorted(res, key=lambda x:(x[2]))       # 按vol_path排序
        return sorted_res


    # 获取上一次检索模式
    def GetLastFilterMode(self):
        res = self.select_from_settings_table('filter_mode')
        if not res:
            return 'common'
        else:
            return res[0]


    # 记录上一次检索模式
    def RecordLastFilterMode(self, filter_mode):
        res = self.select_from_settings_table('filter_mode')
        if not res:
            self.insert_into_settings_table('filter_mode', filter_mode)
        else:
            self.update_settings_table('filter_mode', filter_mode)
    

    # 获取默认检索目录
    def GetDefaultSearchPath(self):
        res = self.select_from_settings_table('default_search_paths')
        if not res:
            return None
        else:
            return res[0].split(', ')


    # 记录默认检索目录
    def SetDefaultSearchPath(self, vol_ids):
        value = ', '.join(map(str, vol_ids))
        res = self.select_from_settings_table('default_search_paths')
        if not res:
            self.insert_into_settings_table('default_search_paths', value)
        else:
            self.update_settings_table('default_search_paths', value)


    # 显示目录下的所有文件（夹）
    def ShowFilesUnderDirByPath(self, target_path):
        # 获取target_path对应的vol的path及name
        target_root_vol_path, target_root_vol_name = '', ''
        for item in self.DisplayPaths():
            vol_id, vol_name, vol_path, dirs_num, files_num, update_time, writing = item
            if writing == 'F':
                if target_path.startswith(vol_path):
                    target_root_vol_path = vol_path
                    target_root_vol_name = vol_name
                    break
        if target_root_vol_path == '' or target_root_vol_name == '':
            print('[ERROR] 已索引的目录中不包含目标文件夹')
            return None

        # 获取target_path在vol中对应的id
        if vol_path == target_path:
            folder_id = 1

        else:
            folder_id = 1
            temp = target_path[len(vol_path):]
            if temp[0] == '\\' or temp[0] == '/':
                temp = temp[1:]
            folder_names = temp.replace('/', '\\').split('\\')

            if not (len(folder_names) == 1 and folder_names[0] == ''):
                success = True
                for folder_name in folder_names:
                    sql = "SELECT * FROM {} WHERE pid={} and name='{}'".format(target_root_vol_name, folder_id, folder_name)
                    self.cur.execute(sql)
                    res = self.cur.fetchall()
                    if len(res) > 0:
                        folder_id = res[0][0]
                    else:
                        success = False
                if not success:
                    print('[ERROR] 已索引的目录中未查找到目标文件夹')
                    return None
        
        # 显示目录下的所有文件（夹）
        return self.ShowFilesUnderDirByID(target_root_vol_name, folder_id)

    
    # 显示目录下的所有文件（夹）
    def ShowFilesUnderDirByID(self, vol_name, target_path_id):
        target_path = self.get_parent(vol_name, target_path_id)

        result = []
        files_num = 0
        dirs_num = 0
        sql = "SELECT id, pid, name, type FROM {} WHERE pid={}".format(vol_name, target_path_id)
        self.cur.execute(sql)
        for one in self.cur.fetchall():
            id, pid, name, type = one

            if type == 'F' or type == 'D':
                parent_path = self.get_parent(vol_name, pid)
                file_path = merge_path(parent_path, name)
            elif type == 'R':
                file_path = name
            
            if type == 'F':
                files_num += 1
            elif type == 'D' or type == 'R':
                dirs_num += 1

            result.append((file_path, type))
        
        print('[LIST] {} 目录下共{}个文件夹，{}个文件'.format(target_path, dirs_num, files_num))
        #print(result)
        return target_path, result, dirs_num, files_num


if __name__ == '__main__':
    root_path = r'Y:\\'
    
    db = MySqlite()
    
    # import time
    # start = time.time()

    # 建立文件索引
    # db.BuildFilesIndex(root_path)

    # end = time.time()
    # print(end - start)

    # 进行文件检索
    # db.SearchFiles(root_path)

    # 进行多vol下文件检索
    # root_path_list = []
    # db.MultiVolSearchFiles(root_path_list, 'yuanshen')

    # 删除文件索引
    # db.DeleteFilesIndex(root_path)

    # 清理无效数据
    # db.CleanInvalidData()

    # 展示已索引目录
    # db.DisplayPaths()

    #db.RecordLastFilterMode('regexp')
    #print(db.GetLastFilterMode())

    # 显示目录下的所有文件（夹）
    target_path = r'D:\Github\crawler\aitaosir'
    db.ShowFilesUnderDirByPath(target_path)