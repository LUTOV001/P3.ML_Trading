

# Submit a batch order that returns completed and uncompleted orders.
def sendBatchOrder(self, qty, stocks, side, resp):
  executed = []
  incomplete = []
  for stock in stocks:
    if(self.blacklist.isdisjoint({stock})):
      respSO = []
      tSubmitOrder = threading.Thread(target=self.submitOrder, args=[qty, stock, side, respSO])
      tSubmitOrder.start()
      tSubmitOrder.join()
      if(not respSO[0]):
      # Stock order did not go through, add it to incomplete.
        incomplete.append(stock)
    else:
      executed.append(stock)
      respSO.clear()
      resp.append([executed, incomplete])
​
# Submit an order if quantity is above 0.
def submitOrder(self, qty, stock, side, resp):
  if(qty > 0):
    try:
      self.alpaca.submit_order(stock, qty, side, "market", "day")
      print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
      resp.append(True)
      except:
      print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
      resp.append(False)
  else:
    print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
    resp.append(True)