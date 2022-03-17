class FlashCategory:
  Info='info'
  Success='success'
  Error='error'
  Warning='warning'

  @staticmethod
  def get_category_and_duration(category: str, duration: int = 5000) -> str:
    return f'{category}:{duration}'
  
  @staticmethod
  def info(duration: int = 5000) -> str:
    return FlashCategory.get_category_and_duration(category=FlashCategory.Info, duration=duration)
  
  @staticmethod
  def success(duration: int = 5000) -> str:
    return FlashCategory.get_category_and_duration(category=FlashCategory.Success, duration=duration)

  @staticmethod
  def warning(duration: int = 5000) -> str:
    return FlashCategory.get_category_and_duration(category=FlashCategory.Warning, duration=duration)

  @staticmethod
  def error(duration: int = 5000) -> str:
    return FlashCategory.get_category_and_duration(category=FlashCategory.Error, duration=duration)
