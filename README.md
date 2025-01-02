# pymycqu

这个库对重庆大学 <https://my.cqu.edu.cn> 和统一身份认证的部分 web api 进行了封装，同时整理了相关数据模型。

Work in progress... 欢迎反馈和补充

感谢 <https://github.com/CQULHW/CQUQueryGrade> 项目提供了 <https://my.cqu.edu.cn> 的登陆方式。

## 安装

```bash
pip install mycqu
```

## 例子及文档

见 <https://pymycqu.hagb.name>.

## 许可

AGPL 3.0


## todo
- [ ] 添加微信或邮箱推送
- [ ] 添加验证码的自动识别，考虑接入一些llm api
- [ ] 添加github action自动部署
- [ ] 按照时间间隔自动查询水电费余额 一卡通余额等设置，或者用户定义的字段
- [ ] 更友好的交互方式
- [ ] 不紧急：添加一个web api，可以查询成绩、课表、电费、一卡通余额等