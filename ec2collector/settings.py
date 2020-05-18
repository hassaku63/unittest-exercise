import os
import dotenv

dotenv.load_dotenv()

AWS_REGION = os.environ.get('AWS_REGION')
TABLE_NAME = os.environ.get('TABLE_NAME')