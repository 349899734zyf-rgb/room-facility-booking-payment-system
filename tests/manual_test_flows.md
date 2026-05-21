# 手动测试流程与分支跳转记录 (Manual Test Flows & Redirections)

本文档记录了基于 `src/test_inputs.csv` 中的测试输入，在本地运行 Monash Study Room Booking System (MSSRB) 时，手动测试输入错误以及特殊支付/预订分支的跳转流程。

---

## 1. 预订流程分支与跳转 (Booking Flows)

### 分支 A：用户主动取消预订 (Cancel Booking Flow)
* **测试输入**:
  1. 登录为学生 `student1@student.monash.edu` / `Password123`。
  2. 选择菜单项 `1. Search & Book Rooms` 进入预订界面。
  3. 当提示输入 `building` (大楼) 时，输入：`CANCEL`。
* **系统表现与跳转**:
  * 控制台打印: `Booking process cancelled.`
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

### 分支 B：无效的时间输入格式 (Invalid Date Input)
* **测试输入**:
  1. 登录为学生 `student1@student.monash.edu`。
  2. 选择菜单项 `1. Search & Book Rooms`。
  3. 大楼输入: `Building A`。
  4. 开始时间输入: `invalid-date`，结束时间输入: `invalid-date`。
* **系统表现与跳转**:
  * 控制台打印: `Invalid input. Please check the building code and time format.`
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

---

## 2. 结账与支付跳转分支 (Checkout & Payment Flows)

测试此项时，模拟预订费用为 `$20.0`。

### 分支 C：余额不足 $\rightarrow$ 选择放弃充值 (Insufficient Funds - Cancel Top-Up)
* **前提条件**: 学生账户余额为 `$5.0`。
* **测试输入**:
  1. 登录为学生 `student1@student.monash.edu`。
  2. 选择菜单项 `2. Checkout & Payment`。
  3. 选择余额支付: `1`。
  4. 提示输入优惠码时，直接回车 (不使用优惠码)。
  5. 系统检测余额不足 (`$5.0 < $20.0`)，提示 `1. Add funds / 2. Stop payment`。
  6. 输入: `2` (放弃充值)。
* **系统表现与跳转**:
  * 控制台打印: `Checkout finished`
  * 账户余额保持为 `$5.0`不变。
  * **跳转目标**: 返回 **Monash Student Portal (学生菜单主界面)**。

### 分支 D：余额不足 $\rightarrow$ 充值成功并确认支付 (Insufficient Funds - Top-Up & Confirm)
* **前提条件**: 学生账户余额为 `$5.0`。
* **测试输入**:
  1. 登录为学生 `student1@student.monash.edu`。
  2. 选择菜单项 `2. Checkout & Payment`。
  3. 选择余额支付: `1`。
  4. 直接回车跳过优惠码。
  5. 提示 `1. Add funds / 2. Stop payment` 时，输入: `1` (选择充值)。
  6. 提示输入充值金额时，输入: `30.0` (充值 `$30.0`，新余额为 `$35.0`)。
  7. 系统提示 `If you want to proceed: 1 for yes, 2 for no`，输入: `1` (确认支付)。
* **系统表现与跳转**:
  * 控制台打印:
    - `Top-up complete. Current balance: $35.0`
    - `Booking confirmed`
    - 显示订单详情 `===== ORDER DETAIL =====` (订单金额为 `$20.0`，新余额扣减为 `$15.0`)。
  * **跳转目标**: 完成扣款后，返回 **Monash Student Portal (学生菜单主界面)**。

---

## 3. 个人资料与设置分支 (Profile & Settings)

### 分支 E：修改电话号码 / 修改密码取消
* **测试输入**:
  1. 选择菜单项 `3. View Profile & Settings` 进入个人资料界面。
  2. 选择修改选项并提示新值输入时，输入 `CANCEL`。
* **系统表现与跳转**:
  * **跳转目标**: 返回 **Student Profile Information (个人资料子菜单)**，不会返回大主界面，允许用户继续做其他修改。
