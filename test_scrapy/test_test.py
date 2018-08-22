def audit_status_change(request, main_travel_id=None, audit_status=None):
	"""
	更改审核状态
	:param request:
	:return:
	"""
	staff = request.user.staff
	# 因为更改主采购订单的状态需要增加财务支出，所以首先判断“零配件采购”是否在平台类别管理中
	# 判断“平台类别管理”中的零配件采购的是否存在
	system_type_father = SystemType.objects.filter(del_status=0, father=None, key="spend1")
	if not system_type_father.exists():
		messages.error(request, "平台类别管理中缺少父类名称为‘日常支出’、key为‘spend1’的父类")
		return HttpResponseRedirect(reverse('main_travel_list') + "?page=" + request.GET.get("page", ""))
	system_type_father = system_type_father[0]
	# 判断“零配件采购”子类别是否有
	system_type_child = SystemType.objects.filter(del_status=0, father=system_type_father, name="差旅费用")
	if not system_type_child.exists():
		messages.error(request, "平台类别管理中缺少父类名称为‘日常支出’的子类别“差旅费用”，请添加")
		return HttpResponseRedirect(reverse('main_travel_list') + "?page=" + request.GET.get("page", ""))
	system_type_child = system_type_child[0]
	# 获取主采购对象
	main_travel = get_object_or_404(MainTravelExpenses, del_status=0, pk=main_travel_id)
	# 如果是提交审核，则需要（提交）增加或者（撤回）修改，否则不需要
	# 如果是提交申请且主采购的状态为未提交，则提交并新增财务支出
	if audit_status == 1 and main_travel.audit_status == 0:
		# 改变主采购订单的状态，为提交
		main_travel.audit_status = audit_status
		main_travel.save()
		# 增加财务支出
		spend = Spend()
		spend.type = system_type_father
		spend.child_type = system_type_child
		# 采购总金额
		spend.price = main_travel.main_travel_total_price()
		spend.explain = "采购订单提交审核"
		# 是否有发票
		spend.receipt = main_travel.is_invoice
		# 申请人
		spend.applicant_staff = staff
		# 申请时间
		spend.applicant_time = datetime.datetime.now().strftime('%Y-%m-%d')
		spend.spent_status = 0
		spend.through_status = 0
		spend.purchase_spend = main_travel
		spend.create_user = staff
		spend.save()
	# 如果是提交申请并且采购的状态为被撤回则修改财务状态
	if audit_status == 1 and main_travel.audit_status == 3:
		# 改变主采购订单的状态，为提交
		main_travel.audit_status = audit_status
		main_travel.save()
		# 获取财务支出信息,并修改状态
		spend = get_object_or_404(Spend, purchase_spend__id=main_travel_id)
		# 采购总金额
		spend.price = main_travel.main_travel_total_price()
		spend.explain = "采购订单被撤回后冲重新提交审核"
		# 是否有发票
		spend.receipt = main_travel.is_invoice
		# 如果为再次修改，如果申请提交后，只有被撤回才会再次修改，只需要判断spend的提交次数就可
		# 如果大于0，就代表已经被撤回，此时给spend再次提交标识
		spend.again_submit_status = 1
		# 给备注附上提交的状态
		spend.save()
	# 如果是确认领款金额
	elif audit_status == 4:
		# 取出财务支出数据，更改状态
		spend = Spend.objects.filter(del_status=0, purchase_spend=main_travel)
		# 首先判断财务那边是否已经打款，禁止恶意操作，直接改变状态
		# spend是否存在
		if not spend.exists():
			messages.error(request, "对应的财务支出数据没有查到，请检查原因！")
			return HttpResponseRedirect(reverse('main_travel_list') + "?page=" + request.GET.get("page", ""))
		spend = spend[0]
		spend_status = spend.spent_status
		# spend_status为2代表着已付款
		if spend_status != 2:
			messages.error(request, "对应的财务支出数据还未付款，采购这边不能进行“领款”操作！")
			return HttpResponseRedirect(reverse('main_travel_list') + "?page=" + request.GET.get("page", ""))
		# 改变主采购订单的状态，为已经领款
		main_travel.audit_status = audit_status
		main_travel.save()
		# 更改财务支出的状态为“领款完毕”
		spend.spent_status = 3
		spend.save()
	return HttpResponseRedirect(reverse('main_travel_list') + "?page=" + request.GET.get("page", ""))
