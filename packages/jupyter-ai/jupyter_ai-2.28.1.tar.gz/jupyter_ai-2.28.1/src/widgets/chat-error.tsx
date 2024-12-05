import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import type { IThemeManager } from '@jupyterlab/apputils';
import { Alert, Box } from '@mui/material';

import { chatIcon } from '../icons';
import { JlThemeProvider } from '../components/jl-theme-provider';

export function buildErrorWidget(
  themeManager: IThemeManager | null
): ReactWidget {
  const ErrorWidget = ReactWidget.create(
    <JlThemeProvider themeManager={themeManager}>
      <Box
        sx={{
          width: '100%',
          height: '100%',
          boxSizing: 'border-box',
          background: 'var(--jp-layout-color0)',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <Box sx={{ padding: 4 }}>
          <Alert severity="error">
            There seems to be a problem with the Chat backend, please look at
            the JupyterLab server logs or contact your administrator to correct
            this problem.
          </Alert>
        </Box>
      </Box>
    </JlThemeProvider>
  );
  ErrorWidget.id = 'jupyter-ai::chat';
  ErrorWidget.title.icon = chatIcon;
  ErrorWidget.title.caption = 'Jupyter AI Chat'; // TODO: i18n

  return ErrorWidget;
}
