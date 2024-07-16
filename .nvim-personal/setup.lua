vim.keymap.set("n", "<f5>", function()
	vim.fn.execute([[term .venv\Scripts\python.exe main.py]])
end, { silent = true, remap = false })
