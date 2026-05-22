# 系统手动测试流程与跳转分支记录

本文档记录了基于 `src/test_inputs.csv` 中的测试输入，在本地运行 Monash Study Room Booking System (MSSRB) 时，手动测试输入错误以及特殊支付/预订分支的跳转流程。

---

## 1. 登录流程分支与跳转

*   **进入路径**：在系统主菜单 (Main Menu) 输入 `1`。

### 分支 A：学生账号成功登录
*   **测试输入**：
    1.  Email：`student1@student.monash.edu`
    2.  Password：`Password123`
*   **系统表现与跳转**：
    *   控制台打印：`Login Successful! Welcome to the Student Portal!`
    *   **跳转目标**：进入 **学生门户主界面 (Monash Student Portal)**。

### 分支 B：管理员账号成功登录
*   **测试输入**：
    1.  Email：`admin1@monash.edu`
    2.  Password：`Password123456`
*   **系统表现与跳转**：
    *   控制台打印：`Login Successful! Welcome to the Admin Portal!`
    *   **跳转目标**：进入 **管理员控制中心界面 (Admin Control Center)**。

### 分支 C：登录凭证错误/认证失败
*   **测试输入**：
    1.  Email：`wrong@student.monash.edu`
    2.  Password：`WrongPassword`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Invalid email or password!`
    *   **跳转目标**：**保持在登录界面** (循环提示重新输入 Email 和密码)。

### 分支 D：用户主动取消登录
*   **测试输入**：
    *   在 Email 或密码输入框中输入：`CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Login cancelled! Returning to main menu.`
    *   **跳转目标**：返回 **系统主菜单 (Main Menu)**。

---

## 2. 注册流程分支与跳转

*   **进入路径**：在系统主菜单 (Main Menu) 输入 `2`。

### 分支 A：新学生成功注册
*   **测试输入**：
    1.  First Name: `Alice`
    2.  Last Name: `Smith`
    3.  Student ID: `00000003` (符合 8 位格式)
    4.  Phone number: `0461812003` (符合 04 开头的 10 位格式)
    5.  Email address: `student3@student.monash.edu` (符合 monash 邮箱后缀)
    6.  Password: `Password123` (包含至少8位，包含大写字母、小写字母及数字)
*   **系统表现与跳转**：
    *   控制台打印：`[SUCCESS] Registration successful! User account created.`
    *   并提示：`Select any key to 'Go to Login'... `，按任意键继续。
    *   **跳转目标**：返回 **系统主菜单 (Main Menu)**。该学生信息将被存入 `students.csv`。

### 分支 B：用户主动取消注册
*   **测试输入**：
    *   在输入任意字段（如 First Name）时，输入：`CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Registration cancelled! Returning to main menu.`
    *   **跳转目标**：返回 **系统主菜单 (Main Menu)**。

### 分支 C：必填字段缺失
*   **测试输入**：
    *   在任意输入项直接按回车（即输入为空白）。
*   **系统表现与跳转**：
    *   控制台打印：`Error: All registration fields are required!`
    *   **跳转目标**：**保持在注册流程中** (重新从 First Name 开始新一轮输入)。

### 分支 D：无效的邮箱域名
*   **测试输入**：
    1.  正常输入姓名、学号和手机号。
    2.  Email address 输入：`student3@gmail.com`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Invalid email domain! Must use @student.monash.edu!`
    *   **跳转目标**：**保持在注册流程中** (循环重新提示输入)。

### 分支 E：密码强度不足
*   **测试输入**：
    1.  正常输入前面字段。
    2.  Email address 输入：`student3@student.monash.edu`
    3.  Password 输入：`123`
*   **系统表现与跳转**：
    *   控制台打印密码强度的限制要求：
        ```
        Password Requirement Message:
        - Password must contain at least 8 characters.
        - Must contain at least 1 uppercase letter.
        - Must contain at least 1 number.
        ```
    *   **跳转目标**：**保持在注册流程中** (循环重新提示输入)。

### 分支 F：重复注册学号或邮箱
*   **测试输入**：
    1.  输入已存在的 ID `00000001` 或 Email `student1@student.monash.edu`。
*   **系统表现与跳转**：
    *   控制台打印：`[ERROR] Registration failed. Email or Student ID may already exist or phone format is invalid.`
    *   **跳转目标**：**保持在注册流程中** (循环重新提示输入)。

### 分支 G：手机号格式错误
*   **测试输入**：
    1.  手机号输入非以 `04` 开头的 10 位数字，例如：`123` 或 `abc`。
*   **系统表现与跳转**：
    *   控制台打印：`[ERROR] Registration failed. Email or Student ID may already exist or phone format is invalid.`
    *   **跳转目标**：**保持在注册流程中** (循环重新提示输入)。

---

## 3. 学生房间搜索与预订流程分支

*   **进入路径**：登录学生账号 -> 在学生菜单输入 `1` 进入房间搜索与预订。
*   **系统预置**：系统中包含一个 `Study Room 1` (R001)，位于大楼 `Building A`，价格为 `$10/hr`，可用时段为 `2026-05-06 10:00-2026-05-06 12:00`。

### 分支 A：成功搜索并预订房间（租借设备，产生押金）
*   **测试输入**：
    1.  Enter building: `Building A`
    2.  Enter start time (YYYY-MM-DD HH:MM): `2026-05-06 10:00`
    3.  Enter end time (YYYY-MM-DD HH:MM): `2026-05-06 12:00`
    4.  Enter room ID to book: `R001`
    5.  Do you want to rent equipment? (1 for Yes, 2 for No): `1`
*   **系统表现与跳转**：
    *   控制台显示租借设备的押金金额（如 `$50.00`），并确认生成未支付订单。
    *   控制台打印：`Success: Booking created successfully!`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 B：成功搜索并预订房间（不租借设备）
*   **测试输入**：
    1.  大楼、时间、房间 ID 均与分支 A 相同。
    2.  Do you want to rent equipment? (1 for Yes, 2 for No) 输入：`2`。
*   **系统表现与跳转**：
    *   只计算房间费用（2小时 * $10/hr = $20.0，设备押金为 $0.0）。
    *   控制台打印：`Success: Booking created successfully!`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 C：用户主动取消预订流程
*   **测试输入**：
    *   在大楼输入、时间输入、选择房间 ID 或选择设备时输入：`CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Booking process cancelled.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**，不保存任何预订。

### 分支 D：时间格式输入错误
*   **测试输入**：
    1.  Enter building: `Building A`
    2.  Enter start time: `invalid-date`
    3.  Enter end time: `invalid-date`
*   **系统表现与跳转**：
    *   控制台打印：`Invalid input. Please check the building code and time format.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 E：持续时间不符合房间类型规则限制
*   **测试前提**：管理员已通过控制台添加了 Medium 类型的房间（单价 `$40.0`），可用时间段为 `2026-05-06 10:00-2026-05-06 12:00`。
*   **测试输入**：
    1.  选择搜索大楼及时间段（如 `2026-05-06 10:00` 到 `2026-05-06 11:00`，共 1 小时）。
    2.  选择该 Medium 房间并尝试预订。
*   **系统表现与跳转**：
    *   根据 Medium Room 的最少 2 小时预订限制，校验失败。
    *   控制台打印：`Error: Minimum duration for Medium/Large rooms is 2 hours.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 F：提前预订天数不符合房间类型规则限制
*   **测试前提**：管理员已通过控制台添加了 Large 类型的房间（单价 `$80.0`），可用时段在当前时间往后 5 小时内。
*   **测试输入**：选择并尝试预订该 Large 房间。
*   **系统表现与跳转**：
    *   根据 Large Room 必须提前 24 小时预订的限制，校验失败。
    *   控制台打印：`Error: Large rooms must be booked at least 24 hours in advance.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 G：选择不存在的房间 ID
*   **测试输入**：
    *   在提示选择房间 ID 时，输入：`RM999`。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Selected room is not available or does not exist.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 H：学生已被禁用阻断预订
*   **前提条件**：当前学生账号状态为 `BANNED`。
*   **测试输入**：在学生菜单输入 `1` 进入房间搜索。
*   **系统表现与跳转**：
    *   系统立即拦截，控制台打印禁用提示及当前未结算活跃订单，不进行房间搜索。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 I：学生已达活跃预订上限阻断预订
*   **前提条件**：学生当前已有 3 个未结账的活跃预订。
*   **测试输入**：在学生菜单输入 `1` 进入房间搜索。
*   **系统表现与跳转**：
    *   系统拦截，控制台打印：`Error: You have reached the limit of 3 active bookings.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

---

## 4. 学生结账与支付流程分支

*   **进入路径**：在学生菜单输入 `2`。
*   **测试前提**：学生 `Student A` 拥有一笔待结账预订，单价为 `$10.0/hr`，时长为 2 小时，未借用设备，金额为 `$20.0`。
*   **优惠码定义**：`NEWBIE20` / `NEWBEE20` (仅 Small 房间可用)。
*   **优惠包定义**：价格为 `$100.0` 购买 12 小时 (仅适用于 Small 房间，且无设备租赁)。

### 分支 A：余额支付 $\rightarrow$ 无优惠码 $\rightarrow$ 确认支付（余额充足）
*   **测试输入**：
    1.  Select a booking to checkout: 选择对应的预订序号。
    2.  Select payment method: 输入 `1` (Balance)。
    3.  Enter promo code: 直接按回车跳过。
    4.  If you want to proceed: 输入 `1` (Yes) 确认。
*   **系统表现与跳转**：
    *   控制台显示订单详情 `===== ORDER DETAIL =====`，扣除余额 `$20.0`（扣减后余额为 `$30.0`）。
    *   控制台打印：`Booking confirmed`
    *   提示后续操作 `1. Continue Booking / 2. Finish`，输入 `2`。
    *   **跳转目标**：打印 `Checkout finished` 并返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 B：余额支付 $\rightarrow$ 使用有效优惠码支付
*   **测试前提**：预订的房间为价格为 `$10.0/hr` 的 Small Room，2 小时费用为 `$20.0`。
*   **测试输入**：
    1.  选择该预订，支付方式选择 `1`。
    2.  优惠码输入：`NEWBIE20` (或 `NEWBEE20`)。
    3.  确认支付选择：`1`。
*   **系统表现与跳转**：
    *   系统校验优惠码有效，享受 20% 折扣，折后应付 `$16.0`。
    *   控制台打印：`Promo code applied. Final price: $16.0`。
    *   **跳转目标**：付款成功后，返回 **学生门户主界面 (Monash Student Portal)**，且该优惠码状态在学生数据中被标记为已使用。

### 分支 C：余额支付 $\rightarrow$ 使用不适用或已使用的优惠码
*   **测试输入**：
    *   对非 Small 房间 (如 Medium/Large 房间) 输入 `NEWBIE20`。
    *   或者输入已被该学生使用过的优惠码。
    *   或者输入不存在的优惠码 `WRONGCODE`。
*   **系统表现与跳转**：
    *   控制台提示优惠码无效或不适用：`Error: Promo code is invalid, expired, or not applicable to this room type.`。
    *   系统退回并重新提示按原价支付，**保持在支付流程中**，可继续完成付款。

### 分支 D：优惠包支付 $\rightarrow$ 满足条件扣减小时数
*   **测试前提**：预订为价格为 `$10.0/hr` 的 Small Room，无设备租赁，且学生账号内已有充足的优惠包时长。
*   **测试输入**：
    1.  选择该预订，支付方式输入 `2` (Deal Package)。
    2.  确认支付选择：`1`。
*   **系统表现与跳转**：
    *   系统自动扣除学生账号对应的优惠包小时数，不扣减现金余额。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 E：优惠包支付 $\rightarrow$ 触发限制拦截（包含设备或非 Small 房间）
*   **测试输入**：
    *   选择包含设备租赁的预订，或选择非 Small 房间预订，支付方式选择 `2` (Deal Package)。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Deal packages can only be used for Small rooms without equipment rentals.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 F：优惠包支付 $\rightarrow$ 小时数不足 $\rightarrow$ 自动重定向购买（余额充足）
*   **测试前提**：预订为 Small Room 2 小时。学生优惠包时长不足，但账户现金余额充足（>= $100.0）。
*   **测试输入**：
    1.  选择支付方式 `2` (Deal Package)。
    2.  系统提示小时数不足，并询问是否购买优惠包，输入 `1` 确认购买。
    3.  确认支付选择：`1`。
*   **系统表现与跳转**：
    *   扣除余额 `$100.0`，充值 12 小时优惠包，随后自动扣减 2 小时完成预订支付。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 G：余额不足支付 $\rightarrow$ 自动重定向充值 $\rightarrow$ 充值成功并确认支付
*   **前提条件**：学生余额为 `$5.0`，待支付金额为 `$20.0`。
*   **测试输入**：
    1.  选择待支付预订，选择对应的预订序号。
    2.  支付方式选择 `1` (Balance)。
    3.  系统检测到余额不足，提示 `1. Add funds / 2. Stop payment`，输入 `1`。
    4.  提示输入充值金额时，输入：`20.0`。
    5.  充值完成后，系统显示账单详情并提示确认是否继续支付订单（"If you want to proceed 1 for yes, 2 for no"），输入：`1`。
*   **系统表现与跳转**：
    *   控制台打印：`Top-up complete. Current balance: $25.0`，扣除 `$20.0` 预订费用，最终余额更新为 `$5.0`。
    *   控制台打印订单详情并显示：`Booking confirmed`。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 H：余额不足支付 $\rightarrow$ 选择停止支付
*   **测试输入**：
    *   当系统提示余额不足并询问是否充值时，输入：`2` (Stop payment)。
*   **系统表现与跳转**：
    *   控制台打印：`Checkout finished`。交易未完成，不产生扣款，订单保持未付状态。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

### 分支 I：用户主动取消支付流程
*   **测试输入**：
    *   在选择预订、选择支付方式、输入优惠码、提示充值选择、输入充值金额、或确认最终支付的任何步骤中输入：`CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Payment cancelled.` 或 `Checkout finished`。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**，不扣除余额和优惠包时长。

---

## 5. 学生个人资料与设置分支

*   **进入路径**：在学生菜单输入 `3` 进入个人资料子选单。

### 5.1 修改手机号 (Update Mobile) - 选项 1
*   **测试选择**：输入 `1`。

#### 分支 A：成功修改手机号
*   **测试输入**：
    1.  Enter new mobile number: `0412345678`
    2.  Confirm new mobile number: `0412345678`
*   **系统表现与跳转**：
    *   控制台打印：`Mobile number updated successfully!`
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 B：修改失败（手机号格式错误）
*   **测试输入**：
    1.  Enter new mobile number: `123` (非 04 开头的 10 位数字)
*   **系统表现与跳转**：
    *   控制台打印：`Error: Invalid mobile format or confirmation mismatch`
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 C：修改失败（两次输入不匹配）
*   **测试输入**：
    1.  Enter new mobile number: `0412345678`
    2.  Confirm new mobile number: `0487654321`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Invalid mobile format or confirmation mismatch`
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 D：主动取消修改手机号
*   **测试输入**：
    *   在输入新手机号或确认手机号时，输入：`CANCEL`。
*   **系统表现与跳转**：
    *   操作被中断，数据无变动。
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

### 5.2 修改密码 (Change Password) - 选项 2
*   **测试选择**：输入 `2`。

#### 分支 A：成功修改密码
*   **测试输入**：
    1.  Enter current password: `Password123`
    2.  Enter new password: `NewPassword123`
    3.  Confirm new password: `NewPassword123`
*   **系统表现与跳转**：
    *   控制台打印：`Password updated successfully!`
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 B：修改失败（原密码错误）
*   **测试输入**：
    1.  Enter current password: `WrongPassword`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Password change failed. Verify credentials or strength.`
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 C：修改失败（密码强度不足）
*   **测试输入**：
    1.  Enter current password: `Password123`
    2.  Enter new password: `123`
*   **系统表现与跳转**：
    *   控制台打印密码强度的限制要求（最少8位，1大写，1数字）。
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 D：修改失败（二次输入确认不匹配）
*   **测试输入**：
    1.  Enter current password: `Password123`
    2.  Enter new password: `NewPassword123`
    3.  Confirm new password: `Mismatch123`
*   **系统表现与跳转**：
    *   控制台打印修改失败的错误提示。
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

#### 分支 E：主动取消修改密码
*   **测试输入**：
    *   在修改密码的任何输入框中输入：`CANCEL`。
*   **系统表现与跳转**：
    *   操作被中断，密码保持原样。
    *   **跳转目标**：保持在 **个人资料子选单 (Profile Sub-menu)** 中。

### 5.3 返回学生菜单 - 选项 3
*   **测试选择**：输入 `3`。
*   **系统表现与跳转**：
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

---

## 6. 学生资金管理分支与跳转

*   **进入路径**：在学生菜单输入 `5` 进入资金管理子选单。

### 分支 A：成功充值
*   **测试输入**：
    1.  Select choice: `1` (Add Funds)
    2.  Enter top-up amount: `100.0`
    3.  Confirm payment? (CONFIRM to authorize): `CONFIRM` (不区分大小写)
*   **系统表现与跳转**：
    *   控制台打印：`Updated Balance: $150.00 (Added Amount: $100.00)`
    *   **跳转目标**：保持在 **资金管理子选单 (Funds Sub-menu)**。

### 分支 B：充值金额格式错误或为负数
*   **测试输入**：
    *   在输入充值金额时输入 `-50` 或非数字 `abc`。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Invalid amount. Values must be strictly positive.` 或 `Error: Please enter a valid numerical dollar currency digit.`
    *   **跳转目标**：保持在 **资金管理子选单 (Funds Sub-menu)**。

### 分支 C：主动取消充值
*   **测试输入**：
    *   在输入金额或确认付款授权时，输入：`CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Payment cancelled. Original balance maintained unchanged.`
    *   **跳转目标**：保持在 **资金管理子选单 (Funds Sub-menu)**，余额无变动。

### 分支 D：返回学生菜单 - 选项 2
*   **测试选择**：输入 `2`。
*   **系统表现与跳转**：
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

---

## 7. 学生使用状态展示分支

*   **进入路径**：在学生菜单输入 `4`。

### 分支 A：展示使用状态
*   **系统表现与跳转**：
    *   控制台输出学生的当前账户使用概况：
        *   当前活跃预订数 (如 `Current Bookings: 1`)
        *   预订限制状态 (如 `Booking Restriction Status: Clear`)
        *   设备押金结清状态 (如 `Equipment Deposit Status: No Outstanding Equipment Deposits`)
        *   当前账户余额 (如 `Balance Status: $50.00`)
    *   并提示：`Press Enter to return to the main portal...`，直接按回车。
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

---

## 8. 学生历史活动账单展示与分页分支

*   **进入路径**：在学生菜单输入 `6`。

### 分支 A：翻页导航
*   **测试输入**：
    *   输入 `1` (Next Page) 转到下一页，或输入 `2` (Previous Page) 返回上一页。
*   **系统表现与跳转**：
    *   历史账单每页展示 2 条流水记录，控制台显示对应的当前页码与总页数。
    *   **跳转目标**：跳转至目标页，且**保持在历史活动账单展示界面**。

### 分支 B：翻页边界警告限制
*   **测试输入**：
    *   在第 1 页输入 `2`。
    *   或者在最后一页输入 `1`。
*   **系统表现与跳转**：
    *   在第 1 页输入 `2` 控制台打印：`You are already displaying the newest transaction records page.`。
    *   在最后一页输入 `1` 控制台打印：`You are already displaying the oldest transaction records page.`。
    *   **跳转目标**：**保持在当前活动账单页面**，页码不发生改变。

### 分支 C：指定页码直接跳转
*   **测试输入**：
    1.  选择指定页码跳转：输入 `3`。
    2.  Enter target page index number: 输入 `2` (有效目标页)。
*   **系统表现与跳转**：
    *   系统成功跳转展示第 2 页的活动流水。
    *   **跳转目标**：**保持在历史活动账单展示界面**。

### 分支 D：跳转页码越界/无效报错
*   **测试输入**：
    1.  选择指定页码跳转：输入 `3`。
    2.  输入无效目标页：`999` 或 `abc`。
*   **系统表现与跳转**：
    *   控制台打印：`[ERROR] Out of range tracking index targets.`
    *   **跳转目标**：**保持在当前活动账单页面**。

### 分支 E：退出账单历史界面
*   **测试输入**：
    *   在导航输入时输入 `4`，或者输入 `CANCEL`。
*   **系统表现与跳转**：
    *   控制台打印：`Returning to main menu.`
    *   **跳转目标**：返回 **学生门户主界面 (Monash Student Portal)**。

---

## 9. 管理员房间管理控制台分支

*   **进入路径**：登录管理员账号 -> 在管理员主选单输入 `1` 进入房间管理。

### 9.1 添加新房间 - 选项 1
*   **测试选择**：输入 `1`。

#### 分支 A：成功添加新房间（自动推断房间类型）
*   **测试输入**：
    1.  Room Name: `Study Pod 2`
    2.  Building: `Building A`
    3.  Capacity: `2`
    4.  Price: `10.0` (因价格低于等于 $10.0/hr，系统判定为 Small Room 类型)
    5.  Opening Hours: `08:00-22:00`
    *(注：房间 ID 将由系统自动按序号递增生成，不需要管理员手动输入。标准设备标准为空，可在后续通过修改房间进行自定义。)*
*   **系统表现与跳转**：
    *   控制台打印：`Success: Room added successfully!`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。
    *   *(注：若 Price 输入低于或等于 10.0，系统自动判定为 Small 类型；若输入在 10.0 与 40.0 之间，系统自动判定为 Medium 类型；若输入高于 40.0，系统判定为 Large 类型。)*

#### 分支 B：添加房间参数输入非数字错误
*   **测试输入**：
    *   在容量 (Capacity) 或价格 (Price) 输入时输入非数字：`abc`。
*   **系统表现与跳转**：
    *   控制台输出对应的格式转换错误（如 `Error: Capacity must be a valid number`）。
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.2 记录推广点子 - 选项 2
*   **测试选择**：输入 `2`。

#### 分支 A：成功记录推广点子
*   **测试输入**：
    *   Enter promotion idea: `10% off for clayton users`
*   **系统表现与跳转**：
    *   控制台打印：`Success: Promotion idea recorded successfully!`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

#### 分支 B：记录失败（内容为空）
*   **测试输入**：
    *   直接回车。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Promotion idea cannot be empty`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.3 修改房间信息 - 选项 8
*   **测试选择**：输入 `8`。

#### 分支 A：成功修改房间信息
*   **测试输入**：
    1.  Enter room ID: `R001` (存在的 ID)
    2.  New room name: `Study Room 1 Updated`
    3.  New capacity: `5`
    4.  New price: `20.0`
    5.  其余项直接按回车留空（留空则不修改，保留原值）。
*   **系统表现与跳转**：
    *   控制台打印：`Success: Room information updated successfully!`，并显示更新后的信息。
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

#### 分支 B：修改失败（房间不存在）
*   **测试输入**：
    1.  Enter room ID: `R999`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Room not found. Please check the room ID.`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

#### 分支 C：修改失败（无任何修改字段）
*   **测试输入**：
    1.  输入存在的 `R001`，后续所有新字段都直接回车。
*   **系统表现与跳转**：
    *   控制台打印：`Error: No information entered to update`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.4 删除房间 - 选项 4
*   **测试选择**：输入 `4`。

#### 分支 A：成功删除房间
*   **测试输入**：
    *   Enter room ID: `R001` (存在的 ID)
*   **系统表现与跳转**：
    *   控制台打印：`Success: Room deleted successfully!`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

#### 分支 B：删除失败（房间不存在）
*   **测试输入**：
    *   Enter room ID: `R999`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Room not found. Please check the room ID.`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.5 更新房间状态 - 选项 5
*   **测试选择**：输入 `5`。
*   **测试输入**：
    1.  Enter room ID: `R001`
    2.  student present: `y`
    3.  equipment rented: `y`
*   **系统表现与跳转**：
    *   控制台打印：`Room status updated successfully`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.6 更新可用时间段 - 选项 6
*   **测试选择**：输入 `6`。

#### 分支 A：成功更新可用时间段
*   **测试输入**：
    1.  Enter room ID: `R001`
    2.  Time slot: `10:00-12:00`
    3.  第二次提示时间段时：直接回车结束。
*   **系统表现与跳转**：
    *   控制台打印：`Success: Room information updated successfully!`
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

#### 分支 B：时间段格式错误
*   **测试输入**：
    1.  Time slot: `invalid-slot`
*   **系统表现与跳转**：
    *   控制台打印：`Error: Format should be HH:MM-HH:MM`
    *   **跳转目标**：**保持在时间段输入流程中** (提示重新输入 Time slot)。

### 9.7 查看预估收入 - 选项 7
*   **测试选择**：输入 `7`。
*   **测试输入**：
    *   Enter room ID: `R001`
*   **系统表现与跳转**：
    *   系统自动根据已占用 slots 乘以单价计提，并打印出该房间的预计收益。
    *   **跳转目标**：保持在 **房间管理控制台 (Admin Room Console)**。

### 9.8 返回主选单 - 选项 3
*   **测试选择**：输入 `3`。
*   **系统表现与跳转**：
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

---

## 10. 管理员更新预订状态与退款分支

*   **进入路径**：在管理员控制中心界面输入 `4`。
*   **测试前提**：学生 `Student A` 拥有对 `R001` 成功付款的预订 `BK001` (总额为 `$70.0`，其中包含 `$20.0` 房间费及 `$50.0` 设备押金)。

### 分支 A：标记为缺席 (No Show) 触发退款与违规计数（根据房间类型退款）
*   **测试输入**：
    1.  Select a booking to update: `BK001`
    2.  Select new status: `5` (No Show)
    3.  Update another booking? (y/n): `n`
*   **系统表现与跳转**：
    *   系统检测到状态修改为缺席，根据该订单所预订的房间类型计算退款：
        *   若预订的为 Small Room (如 `R001`)，将退回 20% 房间费 (`$4.0`) + 100% 设备押金 (`$50.0`)，即共退回 `$54.0`。
        *   若预订的为 Medium/Large 房间，将退回 0% 房间费 + 100% 设备押金，即共退回 `$50.0`。
    *   系统自动将计算出的退款追加至对应的学生账户余额。
    *   该学生的缺席违规次数自动加 1。
    *   该房间的原预约时段重新释放为可用状态。
    *   控制台打印：`Success: Booking status updated successfully!`
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 B：普通状态更新
*   **测试输入**：
    1.  选择 `BK001`。
    2.  新状态输入：`2` (Confirmed) 或 `3` (Completed)。
*   **系统表现与跳转**：
    *   控制台打印：`Success: Booking status updated successfully!`。不发生任何退款和扣罚动作。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 C：更新失败（预订不存在）
*   **测试输入**：
    1.  选择更新的预订 ID：输入 `BK999`。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Booking not found`。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

---

## 11. 管理员学生违规禁令管理与跳转分支

*   **进入路径**：在管理员控制中心界面输入 `2`。

### 分支 A：成功对正常学生实施预订禁令
*   **前提条件**：学生 `00000001` 当前为 ACTIVE 状态。
*   **测试输入**：
    1.  Select student: 输入 `00000001`。
    2.  Are you sure you want to ban? (y/n): 输入 `y`。
    3.  Manage another student? (y/n): 输入 `n`。
*   **系统表现与跳转**：
    *   控制台打印：`Success: Student banned successfully!`，该学生状态被设为 BANNED，无法创建新预约。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 B：成功解除禁用状态的学生
*   **前提条件**：学生 `00000001` 当前为 BANNED 状态。
*   **测试输入**：
    1.  Select student: 输入 `00000001`。
    2.  Are you sure you want to unban? (y/n): 输入 `y`。
    3.  Manage another student? (y/n): 输入 `n`。
*   **系统表现与跳转**：
    *   控制台打印：`Success: Student unbanned successfully!`，该学生状态恢复为 ACTIVE。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 C：操作取消
*   **测试输入**：
    1.  输入任意学生学号，在二次确认时输入 `n`。
*   **系统表现与跳转**：
    *   无任何状态变动。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 D：学生不存在
*   **测试输入**：
    1.  Select student: 输入 `99999999`。
*   **系统表现与跳转**：
    *   控制台打印：`Error: Student not found`。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

---

## 12. 管理员设置设备押金分支与跳转

*   **进入路径**：在管理员控制中心界面输入 `3`。
*   **前提条件**：系统内包含设备 `EQ001`。

### 分支 A：成功修改设备押金金额
*   **测试输入**：
    1.  Select equipment ID: 输入 `EQ001`。
    2.  Enter deposit amount: 输入 `75.0`。
    3.  Confirm setting this deposit amount? (y/n): 输入 `y`。
    4.  Set deposit for another equipment? (y/n): 输入 `n`。
*   **系统表现与跳转**：
    *   设备 `EQ001` 的租赁押金被成功更新为 `$75.00`。
    *   控制台打印：`Success: Equipment deposit amount set to $75.00 successfully!`
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 B：修改失败（金额为负数或格式错误）
*   **测试输入**：
    1.  Select equipment ID: 输入 `EQ001`。
    2.  金额输入：`-20` 或非数字 `abc`。
*   **系统表现与跳转**：
    *   控制台打印相应的报错（如 `Error: Please enter a valid number` 或 `Error: Deposit amount cannot be negative`）。押金金额不发生改变。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。

### 分支 C：修改失败（二次确认选择取消）
*   **测试输入**：
    1.  Select equipment ID: 输入 `EQ001`。
    2.  金额输入：`75.0`。
    3.  二次确认输入：`n`。
*   **系统表现与跳转**：
    *   操作被中断，押金无变化。
    *   **跳转目标**：返回 **管理员控制中心界面 (Admin Control Center)**。
