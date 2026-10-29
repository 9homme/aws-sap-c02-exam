from common import patch
patch("pro-01")
patch("pro-02")
patch("pro-03")
patch("pro-04", "FIX", ["options.A.explanation: อ้างถึง 'ข้อก่อนหน้า' ซึ่งไม่มีความหมายเมื่อสุ่มลำดับข้อสอบ"],
      options={"A": "AD Connector เป็นเพียง proxy ที่ส่งต่อ authentication ไปยัง AD เดิม ไม่ได้สร้าง domain controllers หรือ forest ใหม่ จึงใช้เป็น resource forest และเป็นฝั่งหนึ่งของ forest trust ไม่ได้ AD Connector เหมาะเมื่อบริการ AWS ที่รองรับ เช่น WorkSpaces ต้องใช้ directory เดิมโดยตรง"})
patch("pro-05")
patch("pro-06")
