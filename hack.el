(defun pr ()
  (interactive)
  (let ((default-directory (magit-toplevel)))
    (compile "~/venv3.darwin/bin/prequest development.ini --display-headers / # --header=Accept:text/html" nil)))

(defun test ()
  (interactive)
  (let ((default-directory (magit-toplevel)))
    (compile "~/venv3.darwin/bin/py.test --showlocals tinyurl" nil)))

(defun run ()
  (interactive)
  (let ((default-directory (magit-toplevel)))
    (compile "~/venv3.darwin/bin/pserve --reload development.ini" nil)))
