import os

def extract_urls_recursive(root_dir, output_file):
    """
    递归提取目录及子目录中的.url文件，按文件夹分组输出
    输出格式：
    文件夹名称
    文件名1 URL1
    文件名2 URL2
    """
    result_dict = {}  # 存储目录结构的字典 {目录路径: [(文件名, URL)]}
    
    # 遍历所有子目录
    for foldername, subfolders, filenames in os.walk(root_dir):
        # 获取相对路径（相对于根目录）
        relative_path = os.path.relpath(foldername, root_dir)
        if relative_path == ".":  # 处理根目录的特殊情况
            relative_path = os.path.basename(root_dir)
        
        folder_entries = []
        
        # 处理当前目录的.url文件
        for filename in filenames:
            if not filename.lower().endswith('.url'):
                continue
                
            filepath = os.path.join(foldername, filename)
            url = None
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('URL='):
                            url = line[4:]
                            break
            except Exception as e:
                print(f"读取失败 [{filename}]: {str(e)}")
                continue
            
            if url:
                clean_name = os.path.splitext(filename)[0]
                folder_entries.append( (clean_name, url) )
        
        # 仅保存包含有效数据的目录
        if folder_entries:
            result_dict[relative_path] = folder_entries
    
    # 生成最终输出内容
    output_lines = []
    for path in sorted(result_dict.keys()):
        output_lines.append(f"# {path}")  # 文件夹标题行
        for name, url in result_dict[path]:
            output_lines.append(f"{name} {url}")
        output_lines.append("")  # 添加空行分隔
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"处理完成，结果已保存至 {output_file}")

# 使用示例
extract_urls_recursive(
    root_dir='.\\test\\Web_url',  # 替换为你的根目录
    output_file='.\\test\\organized_urls.txt' #输出目录
)
