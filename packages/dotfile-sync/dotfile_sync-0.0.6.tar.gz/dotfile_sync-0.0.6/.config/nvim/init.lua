local is_unix = vim.loop.os_uname().sysname == 'Linux'
local is_win = vim.loop.os_uname().sysname == 'Windows_NT'

-- Recommended tab config from vim official help
vim.o.softtabstop = 4
vim.o.shiftwidth = 4
vim.o.expandtab = false

-- Turn on this may resolve the hard-to-see issue in nvim under
-- some terminals
vim.o.termguicolors = true
vim.o.number = true

-- Plugins
local Plug = vim.fn['plug#']
vim.call('plug#begin')
-- Manually installed copilot, which is under the 'pack' directory,
-- and this plug managed copilot should not exist simultaneously.
-- Because it may cause laggy input.
Plug('github/copilot.vim')
Plug('preservim/nerdcommenter')
vim.call('plug#end')

-- Config NERDCommenter
vim.g.NERDCreateDefaultMappings = 1
vim.g.NERDSpaceDelims = 1
-- VSCode like keybinding for NERDCommenter
-- The reason why set <C-_> and <C-/> simultaneously for Windows is:
-- https://github.com/wez/wezterm/issues/3180#issuecomment-1517896371
vim.keymap.set('n', '<C-/>', '<Plug>NERDCommenterToggle')
vim.keymap.set('v', '<C-/>', '<Plug>NERDCommenterToggle')
if is_win then
    vim.keymap.set('n', '<C-_>', '<Plug>NERDCommenterToggle')
    vim.keymap.set('v', '<C-_>', '<Plug>NERDCommenterToggle')
end
