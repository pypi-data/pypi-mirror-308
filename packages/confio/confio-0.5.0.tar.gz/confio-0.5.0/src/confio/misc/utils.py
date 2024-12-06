def conf2dict(items: dict):
    """
    将配置项处理成树形对象
    `items` 中， key 为配置项 ID，不包含下级结构
    """
    cache = {}
    result = {}
    for key in items.keys():
        temp = key.split('.')
        value = items[key]
        i = 0
        result_obj = result
        for k in temp:
            i += 1
            temp_key = '.'.join(temp[0:i])
            if temp_key not in cache:
                cache[temp_key] = value if key == temp_key else {}
            if k not in result_obj:
                result_obj[k] = cache[temp_key]
            result_obj = result_obj[k]

    return result


def dict2conf(items: dict):
    """
    将树形对象处理成配置项
    `items` 中，结构为多层结构

    注意：在处理配置值类型为 `dict` 时，结构会与预期不一致
    """
    result = {}

    def flat_object(obj: any, key_path: list):
        if not isinstance(obj, dict):
            result['.'.join(key_path)] = obj
            return

        for key in obj.keys():
            value = obj[key]
            flat_object(value, key_path + [key])

    for k in items.keys():
        flat_object(items[k], [k])

    return result
