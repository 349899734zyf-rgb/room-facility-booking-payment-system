# 手动测试流程与分支跳转记录 (Manual Test Flows & Redirections)

本文档记录了基于 `src/test_inputs.csv` 中的测试输入，在本地运行 Monash Study Room Booking System (MSSRB) 时，手动测试输入错误以及特殊支付/预订分支的跳转流程。

---

## 1. 注册流程分支与跳转 (Registration Flows)

* **进入路径**: 主菜单输入 `2` 进入学生注册界面。

### 分支 A：成功注册 (Successful Registration)
* **测试输入**:
  1. First Name: `Alice`
  2. Last Name: `Smith`
  3. Student ID: `00000003`
  4. Phone number: `0461812003`
  5. Email address: `student3@student.monash.edu`
  6. Password: `Password123` (包含至少8位，1个大写字母，1个数字)
* **系统表现与跳转**:
  * 控制台打印: `[SUCCESS] Registration successful! User account created.`
  * 并提示: `Select any key to 'Go to Login'... `
  * **跳转目标**: 返回 **Main Menu (系统主菜单)**。

### 分支 B：用户主动取消注册 (Cancel Registration)
* **测试输入**:
  * 在输入任意字段（如 First Name）时，输入：`CANCEL`。
* **系统表现与跳转**:
  * 控制台打印: `Registration cancelled! Returning to main menu.`
  * **跳转目标**: 返回 **Main Menu (系统主菜单)**。

### 分支 C：必填字段缺失 (Missing Fields)
* **测试输入**:
  * 在任何输入项直接按回车（例如 First Name 输入为空）。
* **系统表现与跳转**:
  * 控制台打印: `Error: All registration fields are required!`
  * **跳转目标**: **保持在注册流程中** (重新提示输入 First Name 开始新一轮注册输入)。

### 分支 D：无效的邮箱域名 (Invalid Email Domain)
* **测试输入**:
  1. 正常输入姓名、ID和手机号。
  2. Email address 输入: `test@gmail.com`
* **系统表现与跳转**:
  * 控制台打印: `Error: Invalid email domain! Must use @student.monash.edu!`
  * **跳转目标**: **保持在注册流程中** (重新循环提示输入)。

### 分支 E：密码强度不够 (Weak Password)
* **测试输入**:
  1. 正常输入前面的字段。
  2. Email address 输入: `student3@student.monash.edu`
  3. Password 输入: `123`
* **系统表现与跳转**:
  * 控制台打印密码规则提示:
    ```
    Password Requirement Message:
    - Password must contain at least 8 characters.
    - Must contain at least 1 uppercase letter.
    - Must contain at least 1 number.
    ```
  * **跳转目标**: **保持在注册流程中** (重新循环提示输入)。

### 分支 F：重复注册/无效手机号 (Duplicate Credentials or Invalid Phone Format)
* **测试输入**:
  1. 输入已存在的 ID `00000001` 或 Email `student1@student.monash.edu`。
  2. 或者手机号输入格式不正确（如 `123` 不是以04开头的10位数字）。
* **系统表现与跳转**:
  * 控制台打印: `[ERROR] Registration failed. Email or Student ID may already exist or phone format is invalid.`
  * **跳转目标**: **保持在注册流程中** (重新循环提示输入)。

---

## 2. 预订流程分支与跳转 (Booking Flows)

* **进入路径**: 登录学生账号 -> 学生菜单输入 `1. Search & Book Rooms`。

### 分支 G：用户主动取消预订 (Cancel Booking Flow)
* **测试输入**:
  * 在提示输入大楼 `building` 时，输入：`CANCEL`。
* **系统表现与跳转**:
  * 控制台打印: `Booking process cancelled.`
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

### 分支 H：无效的时间输入格式 (Invalid Date Input)
* **测试输入**:
  1. 大楼输入: `Building A`。
  2. 开始时间输入: `invalid-date`，结束时间输入: `invalid-date`。
* **系统表现与跳转**:
  * 控制台打印: `Invalid input. Please check the building code and time format.`
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

---

## 3. 结账与支付跳转分支 (Checkout & Payment Flows)

* **进入路径**: 登录学生账号 -> 学生菜单输入 `2. Checkout & Payment`。
* **测试前提**: 模拟账户有待结账预订，费用为 `$20.0`。

### 分支 I：余额不足 $\rightarrow$ 选择放弃充值 (Insufficient Funds - Cancel Top-Up)
* **前提条件**: 学生账户余额为 `$5.0`。
* **测试输入**:
  1. 选择余额支付: `1`。
  2. 提示输入优惠码时直接回车。
  3. 检测到余额不足，提示 `1. Add funds / 2. Stop payment`，输入: `2`。
* **系统表现与跳转**:
  * 控制台打印: `Checkout finished`
  * 账户余额保持为 `$5.0` 不变。
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

### 分支 J：余额不足 $\rightarrow$ 充值成功并确认支付 (Insufficient Funds - Top-Up & Confirm)
* **前提条件**: 学生账户余额为 `$5.0`。
* **测试输入**:
  1. 选择余额支付: `1`。
  2. 提示输入优惠码时直接回车。
  3. 提示 `1. Add funds / 2. Stop payment` 时，输入: `1`。
  4. 提示输入充值金额时，输入: `30.0`。
  5. 提示 `If you want to proceed: 1 for yes, 2 for no` 时，输入: `1`。
* **系统表现与跳转**:
  * 控制台打印:
    - `Top-up complete. Current balance: $35.0`
    - `Booking confirmed`
    - 显示订单详情 `===== ORDER DETAIL =====` (订单金额为 `$20.0`，新余额扣减为 `$15.0`)。
  * **跳转目标**: 完成扣款后，返回 **Monash Student Portal (学生菜单主界面)**。

---

## 4. 个人资料与设置分支 (Profile & Settings)

* **进入路径**: 登录学生账号 -> 学生菜单输入 `3. View Profile & Settings` 进入个人资料子选单。

### 4.1 修改电话号码 (Update Mobile Number) - 选项 1
* **测试选项**: `1`
* **分支 K：成功修改**
  * 测试输入: 新手机号 `0412345678`，确认手机号 `0412345678`。
  * 系统表现: 控制台打印 `Mobile number updated successfully!`
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。
* **分支 L：用户取消**
  * 测试输入: 新手机号输入 `CANCEL` (或在新手机号输入 `0412345678`，确认手机号输入 `CANCEL`)。
  * 系统表现: 无变动。
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。
* **分支 M：修改失败 (格式错误或确认不匹配)**
  * 测试输入: 新手机号输入 `123` (格式错) 或 确认号输入 `0487654321` (不匹配)。
  * 系统表现: 控制台打印 `Error: Invalid mobile format or confirmation mismatch`
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。

### 4.2 修改密码 (Change Password) - 选项 2
* **测试选项**: `2`
* **分支 N：成功修改**
  * 测试输入: 当前密码 `Password123`，新密码 `NewPassword123`，确认新密码 `NewPassword123`。
  * 系统表现: 控制台打印 `Password updated successfully!`
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。
* **分支 O：用户取消**
  * 测试输入: 当前密码输入 `CANCEL`。
  * 系统表现: 无变动。
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。
* **分支 P：修改失败 (原密码错误、确认不匹配或新密码太弱)**
  * 测试输入: 当前密码输入错误密码，或新密码输入 `123` (太弱)，或确认新密码输入不匹配。
  * 系统表现: 控制台打印密码修改失败的提示。
  * **跳转目标**: 保持在 **Profile Settings Sub-menu (个人资料子菜单)**。

### 4.3 返回主选单 - 选项 3
* **测试选项**: `3`
* **系统表现与跳转**:
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

---

## 5. 资金管理分支与跳转 (Funds Management)

* **进入路径**: 登录学生账号 -> 学生菜单输入 `5. Funds Management` 进入资金管理子选单。

### 分支 Q：成功充值 (Successful Top-Up)
* **测试输入**:
  1. 选择选项: `1` (Add Funds)。
  2. 输入充值金额: `100.0`。
  3. 输入授权确认: `CONFIRM`。
* **系统表现与跳转**:
  * 控制台打印:
    - `Payment Confirmation: Add $100.00 to account?`
    - `[SUCCESS] Payment success message displayed!`
    - `Updated Balance: $150.00 (Added Amount: $100.00)`
  * **跳转目标**: 保持在 **Funds Sub-menu (资金管理子菜单)**。

### 分支 R：取消充值或金额错误 (Cancelled / Invalid Top-Up)
* **测试输入**:
  * 在输入金额时输入 `CANCEL` 或 `abc` 或 `-50`。
  * 或者在输入金额 `100.0` 后，提示授权确认时输入 `CANCEL`。
* **系统表现与跳转**:
  * 控制台打印:
    - 输入 `CANCEL` 时: 退出至资金选项菜单。
    - 输入负数时: `[ERROR] Invalid amount message: Values must be strictly positive.`
    - 输入非数字时: `[ERROR] Please enter a valid numerical dollar currency digit.`
    - 授权输入 `CANCEL` 时: `Payment cancelled. Original balance maintained unchanged.`
  * **跳转目标**: 保持在 **Funds Sub-menu (资金管理子菜单)**。

### 分支 S：返回主选单 (Return to Student Menu)
* **测试输入**:
  * 选择选项: `2` (Return to Main Menu)。
* **系统表现与跳转**:
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

---

## 6. 管理员房间控制台分支与跳转 (Admin Room Console)

* **进入路径**: 登录管理员账号 `admin1@monash.edu` -> 管理员菜单输入 `1. Room Management`。

### 6.1 添加新房间 (Add New Room) - 选项 1
* **测试选项**: `1`
* **分支 T：成功添加房间**
  * 测试输入: Room Name `Study Room 2`, Building `Building A`, Capacity `6`, Price `40.0`, Opening Hours `08:00-22:00`
  * 系统表现: 控制台打印 `Success: Room added successfully!`
  * **跳转目标**: 保持在 **Admin Room Console (管理员房间控制台)**。
* **分支 U：输入校验失败 (价格/容量无效或留空)**
  * 测试输入: 容量输入 `abc` 或 `-2`，或者价格输入 `abc`，或者字段输入为空。
  * 系统表现: 控制台打印对应的错误 (如 `Error: Capacity must be a valid number` 或 `Error: Price must be greater than 0`)。
  * **跳转目标**: 保持在 **Admin Room Console (管理员房间控制台)**。

### 6.2 修改房间信息 (Change Room Information) - 选项 8
* **测试选项**: `8`
* **分支 V：成功修改房间**
  * 测试输入:
    1. Enter room ID: `R001`
    2. New room name: `Study Room 1 Updated`
    3. New capacity: `5`
    4. New price: `20.0`
    5. 其他项直接回车 (留空表示不修改)
  * 系统表现: 控制台打印 `Success: Room information updated successfully!` 并显示更新后的房间详情。
  * **跳转目标**: 保持在 **Admin Room Console (管理员房间控制台)**。
* **分支 W：修改失败 (房间不存在、无更新内容或格式错误)**
  * 测试输入:
    - 房间 ID 输入不存在的 ID `R999` (打印 `Error: Room not found. Please check the room ID.`)
    - 所有修改字段都直接按回车留空 (打印 `Error: No information entered to update`)
    - 修改值输入无效格式如容量为 `abc` (打印 `Error: Capacity must be an integer`)
  * 系统表现: 控制台打印对应错误信息。
  * **跳转目标**: 保持在 **Admin Room Console (管理员房间控制台)**。

---

## 7. 管理员更新预订状态与退款跳转 (Admin Booking Status & Refund)

* **进入路径**: 登录管理员账号 `admin1@monash.edu` -> 管理员菜单输入 `2. Update Booking Status`。
* **测试前提**: 学生 `student1@student.monash.edu` 有一个已付款的预订 `BK001` (费用为 `$20.0`，房间为 Small room 类型的 `R001`)。

### 分支 X：标记为缺席 (No Show) 触发退款与违规计数
* **测试输入**:
  1. 选择要更新的预订 ID: `BK001`
  2. 选择新状态: `5` (No Show)
* **系统表现与跳转**:
  * 系统检测到状态为 `no_show`，触发如下后台逻辑：
    - 根据 Small Room 规则，退款比例为：20% 房间费 (`$20.0 * 20% = $4.0`) + 100% 设备押金。
    - 将退款金额追加到该学生账户余额。
    - 该学生的 No Show 违规计数增加 1。
    - 该预订对应的房间时段重新释放为可用。
    - 控制台打印: `Success: Booking status updated successfully!`
  * 并提示: `Update another booking? (y/n):`，输入 `n`。
  * **跳转目标**: 返回 **Admin Portal Dashboard (管理员主菜单)**。

### 分支 Y：普通状态更新 (Pending/Confirmed/Completed/Cancelled)
* **测试输入**:
  1. 选择要更新的预订 ID: `BK001`
  2. 选择新状态: `2` (Confirmed) 或 `3` (Completed) 等。
* **系统表现与跳转**:
  * 控制台打印: `Success: Booking status updated successfully!`
  * **跳转目标**: 返回 **Admin Portal Dashboard (管理员主菜单)**。

### 分支 Z：更新失败 (预订ID不存在或输入无效状态)
* **测试输入**:
  1. 选择不存在的预订 ID: `BK999` (打印 `Error: Booking not found`)
  2. 或者选择状态时输入无效数字。
* **系统表现与跳转**:
  * 控制台打印对应的错误。
  * **跳转目标**: 返回 **Admin Portal Dashboard (管理员主菜单)**。
