/**
 * MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
 * OHIF Viewer Configuration
 * Albanian Localized Medical Imaging Viewer
 */

window.config = {
  routerBasename: '/viewer',
  
  showStudyList: true,
  showLoadingIndicator: true,
  
  // Default data source - Orthanc
  defaultDataSourceName: 'orthanc',
  
  dataSources: [
    {
      friendlyName: 'MOH Albania PACS',
      namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
      sourceName: 'orthanc',
      configuration: {
        name: 'Orthanc',
        wadoUriRoot: 'http://localhost:8042/wado',
        qidoRoot: 'http://localhost:8042/dicom-web',
        wadoRoot: 'http://localhost:8042/dicom-web',
        qidoSupportsIncludeField: false,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,
        supportsFuzzyMatching: false,
        supportsWildcard: false,
      },
    },
  ],

  // Hotkeys configuration
  hotkeys: [
    {
      commandName: 'incrementActiveViewport',
      label: 'Viewport Tjetër',
      keys: ['right'],
    },
    {
      commandName: 'decrementActiveViewport',
      label: 'Viewport Paraardhës',
      keys: ['left'],
    },
    {
      commandName: 'rotateViewportCW',
      label: 'Rrotullo në drejtim të orës',
      keys: ['r'],
    },
    {
      commandName: 'rotateViewportCCW',
      label: 'Rrotullo kundër drejtimit të orës',
      keys: ['l'],
    },
    {
      commandName: 'flipViewportVertical',
      label: 'Kthe Vertikalisht',
      keys: ['v'],
    },
    {
      commandName: 'flipViewportHorizontal',
      label: 'Kthe Horizontalisht',
      keys: ['h'],
    },
    {
      commandName: 'scaleUpViewport',
      label: 'Zmadho',
      keys: ['+'],
    },
    {
      commandName: 'scaleDownViewport',
      label: 'Zvogëlo',
      keys: ['-'],
    },
    {
      commandName: 'fitViewportToWindow',
      label: 'Përshtat në Dritare',
      keys: ['='],
    },
    {
      commandName: 'resetViewport',
      label: 'Rivendos Pamjen',
      keys: ['space'],
    },
    {
      commandName: 'previousImage',
      label: 'Imazhi Paraardhës',
      keys: ['up'],
    },
    {
      commandName: 'nextImage',
      label: 'Imazhi Pasardhës',
      keys: ['down'],
    },
    {
      commandName: 'toggleCine',
      label: 'Aktivizo/Çaktivizo Cine',
      keys: ['c'],
    },
    {
      commandName: 'invertViewport',
      label: 'Inverso',
      keys: ['i'],
    },
  ],

  // Cornerstonetools settings
  cornerstoneExtensionConfig: {
    tools: {
      ArrowAnnotate: {
        configuration: {
          getTextCallback: (callback) =>
            callback(prompt('Shkruaj shënimin:')),
        },
      },
    },
  },

  // WhiteLabeling - Albanian Ministry Branding
  whiteLabeling: {
    createLogoComponentFn: function (React) {
      return React.createElement(
        'div',
        {
          style: {
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '8px',
          },
        },
        React.createElement(
          'span',
          {
            style: {
              color: '#DC2626',
              fontWeight: 'bold',
              fontSize: '14px',
            },
          },
          'MOH'
        ),
        React.createElement(
          'span',
          {
            style: {
              color: '#1E293B',
              fontSize: '12px',
            },
          },
          'Shqipëri'
        )
      );
    },
  },

  // Customization for toolbar
  customizationService: {
    dicomUploadComponent:
      '@ohif/extension-cornerstone.customizationModule.cornerstoneDicomUploadComponent',
  },

  // MONAI Label extension (if available)
  monaiLabel: {
    enabled: true,
    server: '/monai',
    autoFetch: true,
    autoSegment: false,
  },
};
