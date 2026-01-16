from dify_plugin import Plugin, DifyPluginEnv
from tools.get_chart_of_accounts import GetChartOfAccountsTool
from tools.vendor_management import VendorManagementTool
from tools.create_purchase import CreatePurchaseTool
from tools.create_deposit import CreateDepositTool

plugin = Plugin(DifyPluginEnv())

if __name__ == '__main__':
    plugin.run()
