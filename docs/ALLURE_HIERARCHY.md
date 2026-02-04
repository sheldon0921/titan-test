# Allure 组织结构说明

## 层级关系

Allure 使用分层结构来组织测试报告，从宏观到微观依次是：

```
Feature (功能模块)
  └── Story (用户故事/场景)
        └── Test Case (测试用例 - 含 description)
              └── Step (测试步骤)
              └── Step (测试步骤)
              └── ...
```

## 各层级详解

### 1. @allure.feature - 功能模块（最宏观）

**作用**：描述被测试的**功能模块**或**业务领域**

**特点**：
- 是最高层级的分类
- 通常对应一个业务模块（如用户认证、订单管理、支付模块）
- 在报告中以 Tab 标签页形式展示
- 多个测试用例可以属于同一个 feature

**示例**：
```python
@allure.feature("用户认证模块")
class TestLogin:
    pass

@allure.feature("订单管理模块")
class TestOrder:
    pass

@allure.feature("支付系统")
class TestPayment:
    pass
```

**在报告中展示为**：
```
[用户认证模块] [订单管理模块] [支付系统] (Tab 切换)
```

---

### 2. @allure.story - 用户故事/场景（中观层）

**作用**：描述具体的**业务场景**或**用户故事**

**特点**：
- 从用户视角描述场景
- 一个 feature 下可以有多个 story
- 在报告中以菜单树形式展示
- 对应敏捷开发中的 User Story

**示例**：
```python
@allure.feature("用户认证模块")
class TestLogin:

    @allure.story("登录场景")
    def test_login_with_password(self):
        pass

    @allure.story("注册场景")
    def test_register_new_user(self):
        pass

    @allure.story("密码重置场景")
    def test_reset_password(self):
        pass
```

**在报告中展示为**：
```
用户认证模块
  ├── 登录场景
  │     ├── test_login_with_password
  │     └── test_login_with_sms
  ├── 注册场景
  │     └── test_register_new_user
  └── 密码重置场景
        └── test_reset_password
```

---

### 3. @allure.description - 用例描述（用例层）

**作用**：对单个**测试用例**进行详细说明

**特点**：
- 只能装饰测试函数（不能装饰类）
- 支持 HTML 格式（可以用标签）
- 可以包含测试目的、前置条件、预期结果等
- 在报告的用例详情页显示

**使用方式**：

**方式1：装饰器形式**
```python
@allure.description("""
## 测试目的
验证用户使用正确用户名和密码登录系统的功能

## 前置条件
- 用户已注册
- 用户状态正常

## 测试步骤
1. 输入用户名和密码
2. 点击登录按钮

## 预期结果
- 登录成功
- 跳转到首页
""")
def test_login_success():
    pass
```

**方式2：动态设置**
```python
def test_login_dynamic():
    title = "登录成功场景"
    desc = f"""
    ## 测试场景
    {title}

    ## 测试数据
    - 用户名: admin
    - 密码: 123456
    """
    allure.dynamic.description(desc)
    allure.dynamic.title(title)
```

**在报告中展示为**：
在点击具体测试用例后，详情页顶部显示格式化的描述信息。

---

### 4. @allure.step - 测试步骤（微观层）

**作用**：记录测试执行过程中的**具体步骤**

**特点**：
- 最细粒度的记录
- 支持嵌套（步骤内可以有子步骤）
- 可以添加附件（截图、日志、JSON 等）
- 在报告中以折叠/展开形式展示

**使用方式**：

**方式1：上下文管理器（推荐）**
```python
def test_login():
    with allure.step("步骤1: 打开登录页面"):
        pass

    with allure.step("步骤2: 输入用户名和密码"):
        pass

    with allure.step("步骤3: 点击登录按钮"):
        pass

    with allure.step("步骤4: 验证登录成功"):
        pass
```

**方式2：装饰器**
```python
@allure.step("执行登录操作: {username}")
def login(username, password):
    # 实现登录逻辑
    pass
```

**嵌套示例**：
```python
def test_checkout():
    with allure.step("步骤1: 结账流程"):
        with allure.step("步骤1.1: 查看购物车"):
            pass
        with allure.step("步骤1.2: 选择支付方式"):
            pass
        with allure.step("步骤1.3: 确认支付"):
            pass
```

**在报告中展示为**：
```
测试用例名称
  ├── 步骤1: 打开登录页面
  ├── 步骤2: 输入用户名和密码
  │     └── 附件: 用户信息 (点击展开)
  ├── 步骤3: 点击登录按钮
  └── 步骤4: 验证登录成功
```

---

## 完整示例对比

### 示例 1: 用户登录测试

```python
@allure.feature("用户认证模块")              # ① 功能模块
class TestLogin:

    @allure.story("登录场景")                  # ② 业务场景
    @allure.description("""
    ## 测试目的
    验证用户登录功能的正确性

    ## 测试数据
    - 用户名: admin
    - 密码: 123456
    """)                                        # ③ 用例描述
    def test_login_success(self):
        """测试登录成功场景"""

        # ④ 测试步骤（微观层）
        with allure.step("步骤1: 准备登录数据"):
            username = "admin"
            password = "123456"
            allure.attach(
                f"用户名: {username}\n密码: {'*' * len(password)}",
                name="登录凭证",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("步骤2: 执行登录请求"):
            res = self.auth_api.login(username, password)

        with allure.step("步骤3: 验证响应状态码"):
            assert res.status_code == 200

        with allure.step("步骤4: 验证用户信息"):
            actual_user = get_json_value(res.json(), "$.data.username")
            assert actual_user == username
```

### 在 Allure 报告中的展示结构：

```
[用户认证模块] (Tab)
  ↓
[Behaviors] (左侧导航)
  ├── 登录场景 (Story)
  │     └── test_login_success (用例)
  │           ↓ 点击展开
  │           ┌──────────────────────┐
  │           │ ## 测试目的       │  ← description
  │           │ 验证用户登录功能... │
  │           └──────────────────────┘
  │           ↓
  │           步骤列表:
  │           ✓ 步骤1: 准备登录数据
  │           │   └── 附件: 登录凭证
  │           ✓ 步骤2: 执行登录请求
  │           ✓ 步骤3: 验证响应状态码
  │           ✓ 步骤4: 验证用户信息
```

---

## 最佳实践

### 1. 层级设计原则

| 层级 | 命名规范 | 颗粒度 | 数量建议 |
|------|----------|----------|----------|
| Feature | 名词短语（模块名） | 粗粒度 | 对应业务模块数 |
| Story | 动词短语（场景名） | 中粒度 | 每个模块 3-10 个 |
| Description | Markdown 文档 | 单用例级别 | 每个用例 1 个 |
| Step | 简短动作描述 | 细粒度 | 每个用例 3-8 个 |

### 2. 命名示例

**Feature 命名**：
- ✅ "用户认证模块"
- ✅ "订单管理系统"
- ✅ "支付中心"
- ❌ "测试登录"  (太细)
- ❌ "用户" (太笼统)

**Story 命名**：
- ✅ "登录场景"
- ✅ "注册新用户场景"
- ✅ "密码找回场景"
- ❌ "test_login" (这是函数名)
- ❌ "成功" (不完整)

**Step 命名**：
- ✅ "步骤1: 准备测试数据"
- ✅ "步骤2: 发送登录请求"
- ✅ "步骤3: 验证响应状态"
- ❌ "开始" (不明确)
- ❌ "准备" (缺少编号)

### 3. 使用技巧

**技巧1: 动态设置标题和描述**
```python
def test_dynamic(case_info):
    allure.dynamic.title(case_info['title'])
    allure.dynamic.description(case_info['description'])
```

**技巧2: 在步骤中添加参数**
```python
allure.parameter("用户名", username)
allure.parameter("订单号", order_id)
```

**技巧3: 步骤中添加多种附件**
```python
with allure.step("步骤: 截图验证"):
    allure.attach(screenshot_bytes, "截图", allure.attachment_type.PNG)
    allure.attach(log_text, "日志", allure.attachment_type.TEXT)
    allure.attach(json_data, "响应数据", allure.attachment_type.JSON)
```

**技巧4: 嵌套步骤展示复杂流程**
```python
with allure.step("主流程: 订单结算"):
    with allure.step("子流程: 验证库存"):
        with allure.step("检查商品数量"):
            pass
        with allure.step("锁定商品"):
            pass
    with allure.step("子流程: 创建订单"):
        pass
```

---

## 常见问题

### Q1: 什么时候用 feature，什么时候用 story？
- **Feature**: 描述**功能**（是什么）
- **Story**: 描述**场景**（怎么用）
- 类比：Feature 是"手机"，Story 是"打电话"、"发短信"

### Q2: description 和注释的区别？
- **Description**: 在报告中可见，用于说明测试目的和预期
- **注释**: 在代码中，用于维护和理解代码
- 建议：重要信息放在 description，技术细节放在注释

### Q3: Step 太多会不会影响性能？
- 不会。步骤只是元数据，不影响测试执行速度
- 建议每个用例 3-8 个步骤，过细反而难以阅读

### Q4: 可以在一个测试函数中多次设置 description 吗？
- 不建议。使用 `allure.dynamic.description()` 会覆盖之前的描述
- 建议在函数开始时一次性设置

---

## 总结

```
层级关系：
Feature (宏观 - 功能分类)
  └── Story (中观 - 业务场景)
        └── Description (用例说明)
              └── Test Function
                    └── Step 1
                    └── Step 2
                    └── ...

记忆口诀：
Feature 是模块，Story 是场景
Description 说明用例，Step 记录过程
从大到小，从粗到细
层级清晰，便于追溯
```
