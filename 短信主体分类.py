from typing import Dict, List, Tuple,Dict, Any
import re
#识别发送方主体
def detect_primary_category(text: str, sender: str = "") -> Tuple[str, List[str]]:
    """改进的一级分类检测函数，使用正则表达式优化性能"""

    text_lower = text.lower()
    matched_keywords = []

    # 1. 贷款机构检测 - 最高优先级
    # 构建贷款相关关键词的正则表达式
    loan_sender_keywords = [
        'fecredit', 'homecredit', 'prudential', 'tima', 'akulaku', 'easycredit',
        'miraeasset', 'hd-saison', 'shinhan', 'lotte', 'vnfinance', 'vnpay', 'mpos',
        'capital craft', 'cash crest', 'credit ease', 'flexi credit', 'lend link',
        'myvay', 'prime credit', 'swift funds', 'vaypay', 'soloan', 'tien 24',
        'fin vui', 'vay no', 'viet dong', 'viet dong e', 'viet dong pro', 'vi tot',
        'live cash', 'cash365', 'chia khoa vang', 'fastdong', 'mdong', 'sdong',
        'tieno', '79dong', 'moneyveo', 'vayantoan', 'vaykipthoi', 'tientay24',
        'mekongmobile', 'mar vay', 'okcredit', 'timvay', 'dh loan', 'catcredi', 'catcredit',
        'yocredi', 'think credit', 'kredivo', 'app vay nở', 'ví bắc nam', 'ví tiện lợi',
        'sky credit', 'takomo', 'kdongcredit', 'mcredit', 'tnex finance', 'tnex',
        'tien24', 'tiền24', 'tien 24', 'tiền 24', 'happycredit', 'happycred1t',
        'vamo', 'timo', 'vaycucde', 'vaytienonline', 'oncredit', 'cashwagon',
        'tien24h', 'tiền24h', 'tien24.com', 'tiền24.com', 'tien24vn', 'tiền24vn',
        'tien24 vn', 'tiền24 vn', 'tien24.vn', 'tiền24.vn', 'tien24 online'
    ]
    bank_sender_keywords = [
        'mbbank', 'vietinbank', 'techcombank', 'agribank', 'sacombank', 'eximbank', 'acb',
        'vib', 'ocb', 'hdbank', 'bidv', 'shb', 'vpbank', 'msb', 'tpbank', 'scb', 'seabank',
        'pvcombank', 'kienvietbank', 'lienvietpostbank', 'bacabank', 'abbank', 'dongabank',
        'gpbank', 'kienlongbank', 'namabank', 'ncb', 'oceanbank', 'pgbank', 'saigonbank',
        'vietabank', 'vietcapitalbank', 'publicbank', 'shinhanbank', 'cimb', 'hsbc',
        'standardchartered', 'anz', 'uob', 'wooribank', 'indovinabank', 'vrb', 'tpb',
        'vietcombank', 'shinhan', 'woori', 'cidirect', 'petrolimex'
    ]

    operator_sender_keywords = [
    'viettel', 'vina', 'mobi', 'mobifone', 'vinaphone', 'vietnamobile', 'gmobile',
    'vnpt', 'redsun', 'vietnammobile', 'vtel', 'vnm', 'gh', 'vms', 'viettel_dv',
    'viettel_km', 'viettel_pt', 'viettel_qc', 'mobicloud', 'mobiedu', 'm_service',
    'viettel_post', 'viettel_money', 'myvietteldv', 'critical', 'major', 'clear', 'vt'
    ]
    shopping_sender_keywords = [
        'canifa', 'vascara', 'cayvang', 'fpt', 'aristino', 'cps', 'vietnam post', 'postpay', 'viettel pay',
        'elise', '5s fashion', 'sixdo', 'lotte', 'big c', 'coop', 'guardian', 'pharmacity',
        'circle k', 'ministop', 'gs25', 'bibo mart', 'winmart', 'aeon', 'lotte mart',
        'global mall', 'tiki', 'shopee', 'leika', 'crocs', 'lazada', 'sendo', 'momo',
        'zalopay', 'viettelpay', 'onepay', 'vnpay', 'airpay', 'mypay', 'payoo',
        'hasaki', 'mediamart', 'dienmayxanh', 'nguyen kim', 'thien long', 'vinamilk',
        'uniqlo', 'h&m', 'zara', 'adidas', 'nike', 'puma', 'gucci', 'lv', 'prada'
    ]
    #内容识别
    bank_patterns = r'\b(' + '|'.join([re.escape(bank) for bank in bank_sender_keywords]) + r')\b'
    bank_matches = re.findall(bank_patterns, text_lower)
    matched_keywords.extend(bank_matches)
    if bank_matches:
        return '银行',matched_keywords

    loan_patterns = r'\b(' + '|'.join([re.escape(loan) for loan in loan_sender_keywords]) + r')\b'
    loan_matches = re.findall(loan_patterns, text_lower)
    matched_keywords.extend(loan_matches)
    if loan_matches:
        return '借贷机构',matched_keywords

    operator_patterns = r'\b(' + '|'.join([re.escape(opr) for opr in operator_sender_keywords]) + r')\b'
    operator_matches = re.findall(operator_patterns, text_lower)
    matched_keywords.extend(operator_matches)
    if operator_matches:
        return '运营商', matched_keywords

    shopping_patterns = r'\b(' + '|'.join([re.escape(shop) for shop in shopping_sender_keywords]) + r')\b'
    shopping_matches = re.findall(shopping_patterns, text_lower)
    matched_keywords.extend(shopping_matches)
    if shopping_matches:
        return '购物',matched_keywords

    return '', []

def detect_behavior_category(text: str, sender: str = "") -> Tuple[str, List[str]]:
    text_lower = text.lower()
    matched_keywords = []

    #逾期催收类
    collection_keywords = [
    'nhắc', 'nhac', 'reminder', 'quá hạn', 'qua han', 'trễ hạn', 'tre han', 'đóng tiền',
    'dong tien', 'thanh toan', 'thanh toán', 'nhắc nợ', 'nhac no', 'báo nợ', 'bao no',
    'truy thu', 'thu hồi nợ', 'thu hoi no', 'trốn tránh', 'trốn nợ', 'tranh thủ'
    ]
    collection_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in collection_keywords]) + r')\b'
    collection_matches = re.findall(collection_patterns, text_lower)
    matched_keywords.extend(collection_matches)
    if collection_matches:
        return '逾期催收类', collection_matches

    #还款提醒类
    reminder_keywords = [
    'trả góp', 'tra gop', 'trả nợ', 'tra no', 'hoàn nợ', 'hoan no', 'đáo hạn', 'dao han',
    'quá hạn', 'qua han', 'trễ hạn', 'tre han', 'thanh toan', 'thanh toán', 'tra no',
    'tra gop', 'tới hạn', 'quá hạn', 'quá hạn thanh toán', 'tới hạn thanh toán'
    ]
    reminder_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in reminder_keywords]) + r')\b'
    reminder_matches = re.findall(reminder_patterns, text_lower)
    matched_keywords.extend(reminder_matches)
    if reminder_matches:
        return '逾期催收类', reminder_matches

    #交易通知类
    transaction_keywords = [
        'tk \d+', 'stk \d+', 'so tk \d+', 'tai khoan \d+', 'account \d+',
        'so du', 'balance', 'so du kha dung', 'available balance',
        'chuyen khoan', 'rut tien', 'nap tien', 'thanh toan',
        'transfer', 'withdraw', 'deposit', 'payment',
        'pos', 'atm',
        'jcb', 'visa', 'mastercard', 'amex', 'credit card',
        'the tin dung', '信用卡', 'thẻ tín dụng',
        'ps \d+', 'gd \d+', 'giao dich \d+', 'transaction \d+',
        'han muc', 'han muc kha dung', 'hạn mức', 'hạn mức khả dụng'
    ]
    transaction_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in transaction_keywords]) + r')\b'
    transaction_matches = re.findall(transaction_patterns, text_lower)
    matched_keywords.extend(transaction_matches)
    if transaction_matches:
        return '交易通知类', transaction_matches

    #验证码/授信审批类
    verification_keywords = [
        'otp', 'mã xác thực', 'ma xac thuc', 'xác nhận', 'xac nhan', 'verify', 'mã otp', 'ma otp',
        'xác thực', 'xac thuc', 'mã xác nhận', 'ma xac nhan', 'mat khau', 'password', 'pin'
    ]
    verification_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in verification_keywords]) + r')\b'
    verification_matches = re.findall(verification_patterns, text_lower)
    matched_keywords.extend(verification_matches)
    if verification_matches:
        return '验证码类', verification_matches
################################审批通过/审批拒绝/额度调整未补充############
    #审批通过
    verification1_keywords = [
         'vay', 'cho vay', 'tư vấn', 'tu van', 'hỗ trợ', 'ho tro', 'lãi suất', 'lai suat',
        'tài chính', 'tai chinh', 'tín chấp', 'tin chap', 'thế chấp', 'the chap', 'đăng ký',
        'dang ky', 'sdt', 'hotline', 'zalo', 'lien he', 'call', 'alo', 'chi can', 'khong can'
    ]
    verification1_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in verification1_keywords]) + r')\b'
    verification1_matches = re.findall(verification1_patterns, text_lower)
    matched_keywords.extend(verification1_matches)
    if verification1_matches:
        return '审批通过', verification1_matches

    #审批拒绝
    verification2_keywords = [
        'vay', 'cho vay', 'tư vấn', 'tu van', 'hỗ trợ', 'ho tro', 'lãi suất', 'lai suat',
        'tài chính', 'tai chinh', 'tín chấp', 'tin chap', 'thế chấp', 'the chap', 'đăng ký',
        'dang ky', 'sdt', 'hotline', 'zalo', 'lien he', 'call', 'alo', 'chi can', 'khong can'
    ]
    verification2_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in verification2_keywords]) + r')\b'
    verification2_matches = re.findall(verification2_patterns, text_lower)
    matched_keywords.extend(verification2_matches)
    if verification2_matches:
        return '审批通过', verification2_matches

    # 额度调整
    verification3_keywords = [
        'vay', 'cho vay', 'tư vấn', 'tu van', 'hỗ trợ', 'ho tro', 'lãi suất', 'lai suat',
        'tài chính', 'tai chinh', 'tín chấp', 'tin chap', 'thế chấp', 'the chap', 'đăng ký',
        'dang ky', 'sdt', 'hotline', 'zalo', 'lien he', 'call', 'alo', 'chi can', 'khong can'
    ]
    verification3_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in verification3_keywords]) + r')\b'
    verification3_matches = re.findall(verification3_patterns, text_lower)
    matched_keywords.extend(verification3_matches)
    if verification3_matches:
        return '审批通过', verification3_matches
    
    #营销推广类
    advertiser_keywords = [
        'km', 'khuyen mai', 'khuyến mãi', 'uu dai', 'ưu đãi', 'ctkm',
        'chuong trinh khuyen mai', 'chương trình khuyến mãi',
        'chuong trinh uu dai', 'chương trình ưu đãi',
        'giảm giá', 'giam gia', 'giam', 'giảm', 'discount', 'sale', 'off',
        'giảm sốc', 'giam soc', 'sale sốc', 'sale soc',
        'giá sốc', 'gia soc', 'flash sale', 'sale flash',
        'miễn phí', 'mien phi', 'free', 'zero đ', 'zero d',
        'miễn cước', 'mien cuoc', 'free data', 'free internet',
        'tặng', 'tang', 'tặng thêm', 'tang them', 'bonus', 'quà tặng', 'qua tang'
    ]
    advertiser_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in advertiser_keywords]) + r')\b'
    advertiser_matches = re.findall(advertiser_patterns, text_lower)
    matched_keywords.extend(advertiser_matches)
    if advertiser_matches:
        return '营销推广类', advertiser_matches

    # 服务状态类
    service_keywords = [

    ]
    service_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in service_keywords]) + r')\b'
    service_matches = re.findall(service_patterns, text_lower)
    matched_keywords.extend(service_matches)
    if service_matches:
        return '服务状态类', service_matches

    # 欺诈中介
    decoy_keywords = [

    ]
    decoy_patterns = r'\b(' + '|'.join([re.escape(repay) for repay in decoy_keywords]) + r')\b'
    decoy_matches = re.findall(decoy_patterns, text_lower)
    matched_keywords.extend(decoy_matches)
    if decoy_matches:
        return '欺诈中介', decoy_matches

    return '', []

#金额提取函数
def extract_amount_with_context(text: str) -> List[Dict[str, Any]]:
    """
    增强版上下文感知金额提取函数（带优先级）
    优化了交易金额识别，特别是银行交易格式
    """
    # ====== 0. 预处理 ======
    if not isinstance(text, str) or not text.strip():
        return []

    orig_text = text
    text = re.sub(r'\s+', ' ', text.strip())
    text_lower = text.lower()

    # ====== 1. 高级噪声过滤 ======
    if re.search(r'[a-z0-9]{8,}', text_lower) and not re.search(r'vnd|đ|tr|k', text_lower):
        return []

    # ====== 2. 文本归一化 ======
    text = re.sub(r'[đd₫]|vnd', 'đ', text, flags=re.IGNORECASE)
    text = re.sub(r'\.\s*đ', '000đ', text)
    text = re.sub(r'(\d)([đdktr])', r'\1 \2', text, flags=re.IGNORECASE)

    # ====== 3. 定义金额基础模式 ======
    # 新的金额基础模式 - 能处理带空格的大额数字和符号
    金额基础模式 = r"([+-]?\s*\d[\d\s.,]*\d)\s*(vnd|vnđ|đồng|dong|triệu|tr|k|ngàn|nghìn|nghin|d)?"

    # 支出金额模式
    支出金额_patterns = [
        r"ps\s*" + 金额基础模式,
        r"chi\s*" + 金额基础模式,
        r"thanh\s*toán\s*" + 金额基础模式,
        r"phi\s*" + 金额基础模式,
        r"vnd\s*-\s*" + 金额基础模式,
        r"thanh\s*toan\s*" + 金额基础模式,
        r"ps\s*-\s*" + 金额基础模式,
        r"ps\s*[+-]\s*" + 金额基础模式,
        r"cước\s*" + 金额基础模式,
        r"giá\s*cước\s*" + 金额基础模式,
        r"trả\s*nợ\s*" + 金额基础模式,
        r"tra\s*no\s*" + 金额基础模式,
        r"tiền\s*" + 金额基础模式,
        r"so\s*tien\s*" + 金额基础模式,
        r"thanh toán\s*" + 金额基础模式,
        r"thu\s*" + 金额基础模式,
        r"TK\s+\d+\s+VND\s+-\s+(\d[\d\s.,]*)\s+SD\s+\d[\d\s.,]*"
    ]

    # 收入金额模式
    收入金额_patterns = [
        r"vnd\s*\+\s*" + 金额基础模式,
        r"nap\s*tien\s*" + 金额基础模式,
        r"nạp\s*tiền\s*" + 金额基础模式,
        r"nhan\s*tien\s*" + 金额基础模式,
        r"nhận\s*tiền\s*" + 金额基础模式,
        r"thu\s*" + 金额基础模式,
        r"vnd\s*\+\s*" + 金额基础模式,
        r"hoan\s*tien\s*" + 金额基础模式,
        r"hoàn\s*tiền\s*" + 金额基础模式,
        r"hoan\s*" + 金额基础模式,
        r"lãi\s*suất\s*" + 金额基础模式,
        r"thưởng\s*" + 金额基础模式,
        r"chuyển\s*khoản\s*" + 金额基础模式,
        r"nạp\s*tiền\s*" + 金额基础模式,
        r"TK\s+\d+\s+VND\s+\+\s+(\d[\d\s.,]*)\s+SD\s+\d[\d\s.,]*",
        r"vào\s*[:]?\s*" + 金额基础模式,
        r"vao\s*[:]?\s*" + 金额基础模式,
    ]

    # 交易金额模式 - 优先级最高
    交易金额_patterns = [
        # 银行交易格式
        # r"mbv\s*[+-]\s*" + 金额基础模式,
        r"mbv\s*" + 金额基础模式,
        r"tk\s+\d+\s*" + 金额基础模式,
        r"gd\s*" + 金额基础模式,
        # r"ps\s*[+-]\s*" + 金额基础模式,
        r"ps\s*" + 金额基础模式,
        # 通用交易格式
        r"mua\s*" + 金额基础模式,
        r"chuyển\s*" + 金额基础模式,
        r"gia\s*" + 金额基础模式,
        r"giá\s*trị\s*" + 金额基础模式,
        r"tri\s*gia\s*" + 金额基础模式,
        r"số\s*tiền\s*" + 金额基础模式,
        r"giao dich\s*" + 金额基础模式,
        r"so\s*tien\s*" + 金额基础模式,
        r"gd\s*" + 金额基础模式,
        r"bán\s*" + 金额基础模式,
        r"TK\s+\d+\s+VND\s+([+-])\s+(\d[\d\s.,]*)\s+SD\s+\d[\d\s.,]*",
        r"BIDV\s*" + 金额基础模式,
    ]

    # 余额模式 - 优先级第二
    余额_patterns = [
        # 标准格式
        r"sd\s*[:]?\s*" + 金额基础模式,
        r"s[oố]\s*dư\s*[:]?\s*" + 金额基础模式,
        r"so\s*du\s*[:]?\s*" + 金额基础模式,
        # r"ps\s*[:]?\s*" + 金额基础模式,
        r"tài\s*khoản\s*[:]?\s*" + 金额基础模式,

        # 银行交易格式
        r"TK\s+\d+\s+VND\s+[+-]\s+\d[\d\s.,]*\s+SD\s+(\d[\d\s.,]*)",

        # 严格格式
        r"(?<!\w)sd\s+" + 金额基础模式,
        r"số\s*dư\s*$" + 金额基础模式,
    ]
    信用额度_patterns = [
        r"hạn\s*mức\s*tín\s*dụng\s*" + 金额基础模式,
        r"credit\s*" + 金额基础模式,
        r"tín\s*dụng\s*" + 金额基础模式,
        r"han\s*muc\s*" + 金额基础模式,
        r"han\s*muc\s*tin\s*dung\s*" + 金额基础模式,
        r"tin dung\s*" + 金额基础模式,
        r"hạn mức\s*" + 金额基础模式,
        r"hạn\s*mức\s*" + 金额基础模式
    ]

    放款金额_patterns = [
        r"khoản\s*vay\s*" + 金额基础模式,
        r"giai\s*ngan\s*" + 金额基础模式,
        r"gn\s*" + 金额基础模式,
        r"giải\s*ngân\s*" + 金额基础模式,
        r"vay\s*" + 金额基础模式,
        r"cho\s*vay\s*" + 金额基础模式,
        r"giải\s*ngân\s*" + 金额基础模式,
        r"khoản\s*vay\s*" + 金额基础模式
    ]

    提款金额_patterns = [
        r"chuyển\s*ra\s*" + 金额基础模式,
        r"rt\s*" + 金额基础模式,
        r"rút\s*tiền\s*" + 金额基础模式,
        r"rút\s*" + 金额基础模式,
        r"chuyển\s*khoản\s*" + 金额基础模式,
        r"rut\s*tien\s*" + 金额基础模式,
        r"rút\s*tiền\s*" + 金额基础模式,
        r"chuyển\s*khoản\s*" + 金额基础模式
    ]

    可用余额_patterns = [
        r"số\s*dư\s*khả\s*dụng\s*" + 金额基础模式,
        r"du\s*kha\s*dung\s*" + 金额基础模式,
        r"sd\s*khả\s*dụng\s*" + 金额基础模式,
        r"so\s*du\s*kha\s*dung\s*" + 金额基础模式,
        r"kha\s*dung\s*" + 金额基础模式,
        r"sd\s*kha\s*dung\s*" + 金额基础模式,
        r"so\s*du.*?kha\s*dung\s*" + 金额基础模式
    ]

    逾期金额_patterns = [
        r"qua\s*han\s*" + 金额基础模式,
        r"nợ\s*quá\s*hạn\s*" + 金额基础模式,
        r"nợ\s*" + 金额基础模式,
        r"no\s*" + 金额基础模式,
        r"no\s*qua\s*han\s*" + 金额基础模式,
        r"quá\s*hạn\s*thanh\s*toán\s*" + 金额基础模式,
        r"qua han\s*" + 金额基础模式,
        r"quá\s*hạn\s*" + 金额基础模式,
        r"trễ\s*hạn\s*" + 金额基础模式,
        r"tre\s*han\s*" + 金额基础模式
    ]

    # 新增的金额类型模式
    充值金额_patterns = [
        r"nap\s*the\s*" + 金额基础模式,
        r"nạp\s*thẻ\s*" + 金额基础模式,
        r"nap\s*tien\s*" + 金额基础模式,
        r"nạp\s*tiền\s*" + 金额基础模式,
        r"recharge\s*" + 金额基础模式
    ]

    流量金额_patterns = [
        r"data\s*" + 金额基础模式,
        r"lưu\s*lượng\s*" + 金额基础模式,
        r"luu\s*luong\s*" + 金额基础模式,
        r"gb\s*" + 金额基础模式,
        r"mb\s*" + 金额基础模式
    ]

    套餐费用_patterns = [
        r"gói\s*cước\s*" + 金额基础模式,
        r"goi\s*cuoc\s*" + 金额基础模式,
        r"cước\s*phí\s*" + 金额基础模式,
        r"cuoc\s*phi\s*" + 金额基础模式
    ]

    手续费_patterns = [
        r"phí\s*dịch\s*vụ\s*" + 金额基础模式,
        r"phi\s*dich\s*vu\s*" + 金额基础模式,
        r"phí\s*giao\s*dịch\s*" + 金额基础模式,
        r"phi\s*giao\s*dich\s*" + 金额基础模式
    ]

    罚金_patterns = [
        r"phạt\s*" + 金额基础模式,
        r"phat\s*" + 金额基础模式,
        r"phí\s*phạt\s*" + 金额基础模式,
        r"phi\s*phat\s*" + 金额基础模式
    ]

    # 金额类型映射
    金额类型到patterns = {
        '支出金额': 支出金额_patterns,
        '收入金额': 收入金额_patterns,
        '交易金额': 交易金额_patterns,
        '信用额度': 信用额度_patterns,
        '放款金额': 放款金额_patterns,
        '提款金额': 提款金额_patterns,
        '可用余额': 可用余额_patterns,
        '逾期金额': 逾期金额_patterns,
        '余额': 余额_patterns,
        '充值金额': 充值金额_patterns,
        '流量金额': 流量金额_patterns,
        '套餐费用': 套餐费用_patterns,
        '手续费': 手续费_patterns,
        '罚金': 罚金_patterns
    }

    # 金额提取优先级
    金额类型优先级 = [
        ('交易金额', 交易金额_patterns),
        ('余额', 余额_patterns),
        ('支出金额', 支出金额_patterns),
        ('收入金额', 收入金额_patterns),
        ('提款金额', 提款金额_patterns),
        ('信用额度', 信用额度_patterns),
        ('放款金额', 放款金额_patterns),
        ('可用余额', 可用余额_patterns),
        ('逾期金额', 逾期金额_patterns),
        ('充值金额', 充值金额_patterns),
        ('流量金额', 流量金额_patterns),
        ('套餐费用', 套餐费用_patterns),
        ('手续费', 手续费_patterns),
        ('罚金', 罚金_patterns)
    ]

    # ====== 5. 金额解析函数（保留符号） ======
    def parse_amount(amount_str: str, unit: str) -> float:
        """解析金额字符串并转换为数值，保留符号"""
        # 检查符号
        sign = 1
        if re.match(r'-\s*\d', amount_str):
            sign = -1
            amount_str = re.sub(r'-\s*', '', amount_str)
        elif re.match(r'\+\s*\d', amount_str):
            amount_str = re.sub(r'\+\s*', '', amount_str)
        else:
            sign = 1

        # 移除分隔符
        amount_str = re.sub(r'[ ,.]', '', amount_str)
        # 单位转换
        multiplier = 1
        if unit in ('k', 'ngàn', 'nghìn', 'nghin'):
            multiplier = 1000
        elif unit in ('tr', 'triệu'):
            multiplier = 1000000

        try:
            return sign * float(amount_str) * multiplier
        except ValueError:
            return 0.0

    # ====== 6. 金额提取 ======
    results = []
    matched_texts = set()

    # 按优先级顺序匹配
    for 金额类型, patterns in 金额类型优先级:
        for pattern in patterns:
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                matched_str = match.group(0)
                if matched_str in matched_texts:
                    continue
                # print('match_str',matched_str,'pattern',pattern,'金额类型',金额类型)
                # 提取金额值和单位
                groups = match.groups()
                if len(groups) >= 2:
                    amount_str = groups[0].strip()
                    unit = groups[1].strip() if groups[1] else ""
                else:
                    continue
                # 解析金额
                amount_val = parse_amount(match.group(1), unit)
                if amount_val == 0:  # 允许负值
                    continue

                # 添加上下文片段
                start = max(0, match.start() - 10)
                end = min(len(text_lower), match.end() + 10)
                text_snippet = text_lower[start:end]

                # 添加到结果
                results.append({
                    "amount": amount_val,
                    "unit": "VND",
                    "label": 金额类型,
                    "amount_pattern": pattern,
                    "context": {
                        "text_snippet": text_snippet,
                        "raw_amount": amount_str + (unit if unit else "")
                    }
                })

                # 记录已匹配文本
                matched_texts.add(matched_str)

                # 限制最多5个金额字段
                if len(results) >= 5:
                    break

    # ====== 7. 上下文标签校正 ======
    context_labels = {
        '余额': ['so du', 'số dư', 'sd', 'ps', 'tk', 'sodu'],
        '收入金额': ['vào', 'vao', 'nap tien', 'nạp tiền'],
        '交易金额': ['ps', 'tk', 'mb', 'acb', 'vib', 'chuyen', 'chuyển', 'giao dich', 'mbv', 'gd', 'thanh toan', 'huy thanh toan'],
        '支出金额': ['thanh toan', 'chi', 'phi', 'ps', 'rút', 'rut'],
        '银行账号': ['mb', 'tk', 'acb', 'vcb', 'stk', 'số tài khoản']
    }

    for res in results:
        # 获取当前标签的关键词
        current_label = res["label"]
        current_keywords = context_labels.get(current_label, [])

        # 检查当前标签的关键词是否在上下文片段中出现
        current_label_match = any(
            re.search(kw, res["context"]["text_snippet"])
            for kw in current_keywords
        )

        # 如果当前标签的关键词存在，保留当前标签
        if current_label_match:
            continue

        # 否则，尝试校正为其他标签
        for label, keywords in context_labels.items():
            if label == current_label:
                continue

            if any(re.search(kw, res["context"]["text_snippet"]) for kw in keywords):
                res["label"] = label
                break
    # print(results)
    # 过滤掉银行账号
    results = [res for res in results if res["label"] != "银行账号"]
    # ====== 8. 后处理 ======
    # 定义需要金额范围限制的标签
    restricted_labels = {'交易金额', '收入金额', '支出金额'}

    # 对特定标签添加金额范围过滤 - 舍弃大于99999999或小于100的金额
    filtered_results = []
    for res in results:
        if res["label"] in restricted_labels:
            # 对限制的标签进行金额范围检查
            if 100 <= abs(res['amount']) <= 999999999:
                filtered_results.append(res)
        else:
            # 其他标签的金额不过滤
            filtered_results.append(res)

    # 去重
    unique_results = []
    seen = set()
    for res in filtered_results:
        key = (res["amount"], res["label"])
        if key not in seen:
            unique_results.append(res)
            seen.add(key)

    return unique_results